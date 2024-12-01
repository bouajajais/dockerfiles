import os
from ..base.images import get_target_image as get_target_image_base

CURRENT_DIR = os.path.dirname(__file__)
IMAGE_NAME = os.path.basename(CURRENT_DIR)
    
def get_cuda_tag(config: dict) -> str:
    cuda_version = config["cuda_version"]
    cuda_cudnn = "" if config["cuda_cudnn"] == "" else f"-{config['cuda_cudnn']}"
    cuda_type = "" if config["cuda_type"] == "" else f"-{config['cuda_type']}"
    cuda_os = "" if config["cuda_os"] == "" else f"-{config['cuda_os']}"
    return f"{cuda_version}{cuda_cudnn}{cuda_type}{cuda_os}"

def get_cuda_config(cuda_tag: str) -> dict:
    cuda_tag_details = cuda_tag.split("-")
    cuda_version = cuda_tag_details[0]
    
    cuda_cudnn = ""
    if "cudnn" in cuda_tag_details:
        cuda_cudnn = "cudnn"
    
    cuda_type = ""
    if "base" in cuda_tag_details:
        cuda_type = "base"
    elif "devel" in cuda_tag_details:
        cuda_type = "devel"
    elif "runtime" in cuda_tag_details:
        cuda_type = "runtime"
    
    cuda_os = ""
    if cuda_tag_details[-1] not in (cuda_version, cuda_cudnn, cuda_type):
        cuda_os = cuda_tag_details[-1]
    
    return {
        "cuda_version": cuda_version,
        "cuda_cudnn": cuda_cudnn,
        "cuda_type": cuda_type,
        "cuda_os": cuda_os,
    }

def get_target_image(config: dict) -> str | None:
    if config["target"] not in ("base", "dev-base"):
        return None
    
    docker_user = config["docker_user"]
    image_name = IMAGE_NAME
    target_suffix = "" if config["target"] == "base" else "--dev"
    return f"{docker_user}/{image_name}:{get_cuda_tag(config)}{target_suffix}"

def get_config(target_image: str) -> dict:
    docker_user, image = target_image.split("/")[-1]
    image_tag = image.split(":")[-1]
    cuda_tag = image_tag.split("--")[0]
    
    return {
        "docker_user": docker_user,
        "target": f"{'dev-' if target_image.endswith("--dev") else ''}base",
        **get_cuda_config(cuda_tag)
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