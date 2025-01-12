import os
from utilities import construct_image_tag, get_image_from_infos, get_image_infos, parse_image_tag
from dockerfiles.cuda.images import get_target_image as get_target_image_cuda, get_cuda_tag, get_cuda_config

CURRENT_DIR = os.path.dirname(__file__)
IMAGE_BASENAME = os.path.basename(CURRENT_DIR).replace("_", "-")
HAS_NO_TAG = False

def get_target_image(config: dict) -> str | None:
    if config["target"] not in ("prod", "dev"):
        return None
    
    cuda_image = f"nvidia/cuda:{get_cuda_tag(config)}"
    python_image = f"python:{config['python_version']}"
    return get_image_from_infos({
        "image_user": config["docker_user"],
        "image_basename": IMAGE_BASENAME,
        "image_tag": construct_image_tag({
            "images_infos": [
                get_image_infos(cuda_image),
                get_image_infos(python_image),
            ],
            "target": config["target"]
        })
    })

def get_config(image: str) -> dict:
    image_infos = get_image_infos(image)
    parsed_image = parse_image_tag(image_infos["image_tag"])
    cuda_config = get_cuda_config(parsed_image["images_infos"][0]["image_tag"])
    python_version = parsed_image["images_infos"][1]["image_tag"]
    
    return {
        "docker_user": image_infos["image_user"],
        "target": parsed_image["target"],
        "cuda_version": cuda_config["cuda_version"],
        "cuda_cudnn": cuda_config["cuda_cudnn"],
        "cuda_type": cuda_config["cuda_type"],
        "cuda_os": cuda_config["cuda_os"],
        "python_version": python_version,
    }
        
def get_target_images(partial_args: dict) -> list[str]:
    target_images = []
    docker_user = partial_args["docker_user"]
    for target in partial_args["target"]:
        for cuda_version in partial_args["cuda_version"]:
            for cuda_cudnn in partial_args["cuda_cudnn"]:
                for cuda_type in partial_args["cuda_type"]:
                    for cuda_os in partial_args["cuda_os"]:
                        for python_version in partial_args["python_version"]:
                            target_image = get_target_image({
                                "docker_user": docker_user,
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
    return get_target_image_cuda({
        "docker_user": config["docker_user"],
        "target": config["target"],
        "cuda_version": config["cuda_version"],
        "cuda_cudnn": config["cuda_cudnn"],
        "cuda_type": config["cuda_type"],
        "cuda_os": config["cuda_os"],
    })
    
def get_build_args(target_image: str) -> dict:
    config = get_config(target_image)
    build_args = {}
    build_args["CUDA_TAG"] = get_cuda_tag(config)
    build_args["PYTHON_VERSION"] = config["python_version"]
    return build_args