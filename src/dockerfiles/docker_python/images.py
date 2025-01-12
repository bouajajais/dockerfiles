import os
from utilities import construct_image_tag, get_image_from_infos, get_image_infos, parse_image_tag
from dockerfiles.docker.images import get_target_image as get_target_image_docker

CURRENT_DIR = os.path.dirname(__file__)
IMAGE_BASENAME = os.path.basename(CURRENT_DIR).replace("_", "-")
HAS_NO_TAG = False

def get_target_image(config: dict) -> str | None:
    if config["target"] not in ("prod", "dev"):
        return None
    
    docker_image = f"docker:{config['docker_tag']}"
    python_image = f"python:{config['python_version']}"
    return get_image_from_infos({
        "image_user": config["docker_user"],
        "image_basename": IMAGE_BASENAME,
        "image_tag": construct_image_tag({
            "images_infos": [
                get_image_infos(docker_image),
                get_image_infos(python_image)
            ],
            "target": config["target"]
        })
    })

def get_config(image: str) -> dict:
    image_infos = get_image_infos(image)
    parsed_image = parse_image_tag(image_infos["image_tag"])
    docker_tag = parsed_image["images_infos"][0]["image_tag"]
    python_version = parsed_image["images_infos"][1]["image_tag"]
    
    return {
        "docker_user": image_infos["image_user"],
        "target": parsed_image["target"],
        "docker_tag": docker_tag,
        "python_version": python_version,
    }
        
def get_target_images(partial_args: dict) -> list[str]:
    target_images = []
    docker_user = partial_args["docker_user"]
    for target in partial_args["target"]:
        for docker_tag in partial_args["docker_tag"]:
            for python_version in partial_args["python_version"]:
                config = {
                    "docker_user": docker_user,
                    "target": target,
                    "docker_tag": docker_tag,
                    "python_version": python_version,
                }
                target_image = get_target_image(config)
                if target_image is not None:
                    target_images.append(target_image)
                            
    return target_images

def get_dependency(target_image: str) -> str:
    config = get_config(target_image)
    return get_target_image_docker({
        "docker_user": config["docker_user"],
        "target": config["target"],
        "docker_tag": config["docker_tag"]
    })
    
def get_build_args(target_image: str) -> dict:
    config = get_config(target_image)
    build_args = {}
    build_args["DOCKER_TAG"] = config["docker_tag"]
    build_args["PYTHON_VERSION"] = config["python_version"]
    return build_args