import os
from ..cuda.images import get_target_image as get_target_image_cuda, get_cuda_tag, get_cuda_config

CURRENT_DIR = os.path.dirname(__file__)
IMAGE_NAME = os.path.basename(CURRENT_DIR)

def get_target_image(config: dict) -> str | None:
    if config["target"] not in ("base", "dev-base"):
        return None
    
    docker_user = config["docker_user"]
    image_name = IMAGE_NAME
    python_version = config["python_version"]
    target_suffix = "" if config["target"] == "base" else "--dev"
    return f"{docker_user}/{image_name}:{get_cuda_tag(config)}--python-{python_version}{target_suffix}"

def get_config(target_image: str) -> dict:
    docker_user, image = target_image.split("/")[-1]
    image_tag = image.split(":")[-1]
    meta_details = image_tag.split("--")
    cuda_tag = meta_details[0]
    
    return {
        "docker_user": docker_user,
        "target": f"{'dev-' if target_image.endswith("--dev") else ''}base",
        **get_cuda_config(cuda_tag),
        "python_version": meta_details[1].split("-")[1],
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
                        for python_version in partial_args["python_version"]:
                            target_image = get_target_image({
                                "docker_user": partial_args["docker_user"],
                                "target": target,
                                "cuda_version": cuda_version,
                                "cuda_cudnn": cuda_cudnn,
                                "cuda_type": cuda_type,
                                "cuda_os": cuda_os,
                                "python_version": python_version,
                            })
                            if target_image is not None:
                                target_images.append(target_image)
                            
    return target_images

def get_dependency(target_image: str) -> str:
    config = get_config(target_image)
    return get_target_image_cuda(config)
    
def build(target_image: str) -> None:
    config = get_config(target_image)
    build_args = {}
    build_args["CUDA_TAG"] = get_cuda_tag(config)
    build_args["PYTHON_VERSION"] = config["python_version"]
    joint_build_args = " ".join([f'--build-arg {k}="{v}"' for k, v in build_args.items() if v is not None])
    docker_cmd = f"docker build {joint_build_args} --target {config['target']} -t {target_image} ."
    os.system(f"cd {CURRENT_DIR} && {docker_cmd}")