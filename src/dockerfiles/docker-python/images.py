import os
from ...utilities import construct_image_tag, get_image_from_infos, get_image_infos, parse_image_tag
from ..docker.images import get_target_image as get_target_image_docker

CURRENT_DIR = os.path.dirname(__file__)
IMAGE_BASENAME = os.path.basename(CURRENT_DIR)

def get_python_tag(config: dict) -> str:
    python_version = config["python_version"]
    python_type = "" if config["python_type"] == "" else f"-{config['python_type']}"
    python_os = "" if config["python_os"] == "" else f"-{config['python_os']}"
    return f"{python_version}{python_type}{python_os}"

def get_python_config(python_tag: str) -> dict:
    python_tag_details = python_tag.split("-")
    python_version = python_tag_details[0]
    
    python_type = ""
    if "slim" in python_tag_details:
        python_type = "slim"
    
    python_os = ""
    if python_tag_details[-1] not in (python_version, python_type):
        python_os = python_tag_details[-1]
    
    return {
        "python_version": python_version,
        "python_type": python_type,
        "python_os": python_os,
    }

def get_target_image(config: dict) -> str | None:
    if config["target"] not in ("prod", "dev"):
        return None
    
    docker_image = f"docker:{config['docker_tag']}"
    python_image = f"python:{get_python_tag(config)}"
    return get_image_from_infos({
        "image_user": config["docker_user"],
        "image_basename": IMAGE_BASENAME,
        "image_tag": construct_image_tag(
            [
                get_image_infos(docker_image),
                get_image_infos(python_image)
            ],
            config["target"]
        )
    })

def get_config(target_image: str) -> dict:
    docker_user, image = target_image.split("/")[-1]
    image_tag = image.split(":")[-1]
    python_tag = image_tag.split("--")[0]
    
    return {
        "docker_user": docker_user,
        "target": f"{'dev-' if target_image.endswith("--dev") else ''}base",
        **get_python_config(python_tag)
    }
        
def get_target_images(partial_args: dict) -> list[str]:
    target_images = []
    
    for target in partial_args["target"]:
        if target not in ("base", "dev-base"):
            continue
    
        for cuda_version in partial_args["cuda_version"]:
            for cuda_cudnn in partial_args["cuda_cudnn"]:
                for cuda_type in partial_args["cuda_type"]:
                    for cuda_os in partial_args["cuda_os"]:
                        target_image = get_target_image({
                            "docker_user": partial_args["docker_user"],
                            "target": target,
                            "cuda_version": cuda_version,
                            "cuda_cudnn": cuda_cudnn,
                            "cuda_type": cuda_type,
                            "cuda_os": cuda_os,
                        })
                        if target_image is not None:
                            target_images.append(target_image)
                            
    return target_images

def get_dependency(target_image: str) -> str:
    config = get_config(target_image)
    return get_target_image_base({
        "docker_user": config["docker_user"],
        "target": config["target"],
        "base_image": f"nvidia/cuda:{get_cuda_tag(config)}"
    })
    
def build(target_image: str) -> None:
    config = get_config(target_image)
    build_args = {}
    build_args["CUDA_TAG"] = get_cuda_tag(config)
    joint_build_args = " ".join([f'--build-arg {k}="{v}"' for k, v in build_args.items() if v is not None])
    docker_cmd = f"docker build {joint_build_args} --target {config['target']} -t {target_image} ."
    os.system(f"cd {CURRENT_DIR} && {docker_cmd}")