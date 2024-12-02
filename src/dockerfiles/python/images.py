import os
from utilities import construct_image_tag, get_image_from_infos, get_image_infos, parse_image_tag
from dockerfiles.base.images import get_target_image as get_target_image_base

CURRENT_DIR = os.path.dirname(__file__)
IMAGE_BASENAME = os.path.basename(CURRENT_DIR).replace("_", "-")

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
    
    python_image = f"python:{get_python_tag(config)}"
    return get_image_from_infos({
        "image_user": config["docker_user"],
        "image_basename": IMAGE_BASENAME,
        "image_tag": construct_image_tag(
            [get_image_infos(python_image)],
            config["target"]
        )
    })

def get_config(image: str) -> dict:
    image_infos = get_image_infos(image)
    parsed_image = parse_image_tag(image_infos["image_tag"])
    python_tag = parsed_image["images_infos"][0]["image_tag"]
    
    return {
        "docker_user": image_infos["image_user"],
        "target": parsed_image["target"],
        **get_python_config(python_tag)
    }
        
def get_target_images(partial_args: dict) -> list[str]:
    target_images = []
    docker_user = partial_args["docker_user"]
    for target in partial_args["target"]:
        for python_version in partial_args["python_version"]:
            for python_type in partial_args["python_type"]:
                for python_os in partial_args["python_os"]:
                    target_image = get_target_image({
                        "docker_user": docker_user,
                        "target": target,
                        "python_version": python_version,
                        "python_type": python_type,
                        "python_os": python_os
                    })
                    if target_image is not None:
                        target_images.append(target_image)
    return target_images

def get_dependency(target_image: str) -> str:
    config = get_config(target_image)
    return get_target_image_base({
        "docker_user": config["docker_user"],
        "target": config["target"],
        "base_image": f"python:{get_python_tag(config)}"
    })
    
def get_build_args(target_image: str) -> dict:
    config = get_config(target_image)
    build_args = {}
    build_args["PYTHON_TAG"] = get_python_tag(config)
    return build_args