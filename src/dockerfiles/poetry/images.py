import os
from utilities import construct_image_tag, get_image_from_infos, get_image_infos, parse_image_tag
from dockerfiles.python.images import get_target_image as get_target_image_python, get_python_tag, get_python_config

CURRENT_DIR = os.path.dirname(__file__)
IMAGE_BASENAME = os.path.basename(CURRENT_DIR).replace("_", "-")
HAS_NO_TAG = False

def get_target_image(config: dict) -> str | None:
    if ("alpine" not in config["python_os"] and config["target"] not in ("prod", "dev")) \
        or ("alpine" in config["python_os"] and config["target"] not in ("alpine-prod", "alpine-dev")):
        return None
    
    poetry_image = f"poetry:{config['poetry_version']}"
    python_image = f"python:{get_python_tag(config)}"
    return get_image_from_infos({
        "image_user": config["docker_user"],
        "image_basename": IMAGE_BASENAME,
        "image_tag": construct_image_tag({
            "images_infos": [
                get_image_infos(poetry_image),
                get_image_infos(python_image)
            ],
            "target": config["target"]
        })
    })

def get_config(image: str) -> dict:
    image_infos = get_image_infos(image)
    parsed_image = parse_image_tag(image_infos["image_tag"])
    poetry_version = parsed_image["images_infos"][0]["image_tag"]
    python_config = get_python_config(parsed_image["images_infos"][1]["image_tag"])
    
    return {
        "docker_user": image_infos["image_user"],
        "target": parsed_image["target"],
        "poetry_version": poetry_version,
        "python_version": python_config["python_version"],
        "python_type": python_config["python_type"],
        "python_os": python_config["python_os"],
    }
        
def get_target_images(partial_args: dict) -> list[str]:
    target_images = []
    docker_user = partial_args["docker_user"]
    for target in partial_args["target"]:
        for poetry_version in partial_args["poetry_version"]:
            for python_version in partial_args["python_version"]:
                for python_type in partial_args["python_type"]:
                    for python_os in partial_args["python_os"]:
                        config = {
                            "docker_user": docker_user,
                            "target": target,
                            "poetry_version": poetry_version,
                            "python_version": python_version,
                            "python_type": python_type,
                            "python_os": python_os,
                        }
                        target_image = get_target_image(config)
                        if target_image is not None:
                            target_images.append(target_image)
    return target_images

def get_dependency(target_image: str) -> str:
    config = get_config(target_image)
    return get_target_image_python({
        "docker_user": config["docker_user"],
        "target": config["target"],
        "python_version": config["python_version"],
        "python_type": config["python_type"],
        "python_os": config["python_os"]
    })
    
def get_build_args(target_image: str) -> dict:
    config = get_config(target_image)
    build_args = {}
    build_args["POETRY_VERSION"] = config["poetry_version"]
    build_args["PYTHON_TAG"] = get_python_tag({
        "python_version": config["python_version"],
        "python_type": config["python_type"],
        "python_os": config["python_os"]
    })
    return build_args