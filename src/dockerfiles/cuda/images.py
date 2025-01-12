import os
from utilities import construct_image_tag, get_image_from_infos, get_image_infos, parse_image_tag
from dockerfiles.base.images import get_target_image as get_target_image_base

CURRENT_DIR = os.path.dirname(__file__)
IMAGE_BASENAME = os.path.basename(CURRENT_DIR).replace("_", "-")
HAS_NO_TAG = False

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
    if config["target"] not in ("prod", "dev"):
        return None
    
    cuda_image = f"nvidia/cuda:{get_cuda_tag(config)}"
    return get_image_from_infos({
        "image_user": config["docker_user"],
        "image_basename": IMAGE_BASENAME,
        "image_tag": construct_image_tag({
            "images_infos": [get_image_infos(cuda_image)],
            "target": config["target"]
        })
    })

def get_config(image: str) -> dict:
    image_infos = get_image_infos(image)
    parsed_image = parse_image_tag(image_infos["image_tag"])
    cuda_tag = parsed_image["images_infos"][0]["image_tag"]
    
    return {
        "docker_user": image_infos["image_user"],
        "target": parsed_image["target"],
        **get_cuda_config(cuda_tag)
    }
        
def get_target_images(partial_args: dict) -> list[str]:
    target_images = []
    docker_user = partial_args["docker_user"]
    for target in partial_args["target"]:
        for cuda_version in partial_args["cuda_version"]:
            for cuda_cudnn in partial_args["cuda_cudnn"]:
                for cuda_type in partial_args["cuda_type"]:
                    for cuda_os in partial_args["cuda_os"]:
                        target_image = get_target_image({
                            "docker_user": docker_user,
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
    
def get_build_args(target_image: str) -> dict:
    config = get_config(target_image)
    build_args = {}
    build_args["CUDA_TAG"] = get_cuda_tag(config)
    return build_args