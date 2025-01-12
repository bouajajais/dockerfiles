import os
from typing import TypedDict
from utilities import Target, get_image_infos, get_image_from_infos, construct_image_tag, parse_image_tag

CURRENT_DIR = os.path.dirname(__file__)
IMAGE_BASENAME = os.path.basename(CURRENT_DIR).replace("_", "-")
HAS_NO_TAG = False

class Config(TypedDict):
    docker_user: str
    target: Target
    base_image: str


def get_target_image(config: Config) -> str | None:
    if config["target"] not in ("prod", "dev", "alpine-prod", "alpine-dev"):
        return None
    
    return get_image_from_infos({
        "image_user": config["docker_user"],
        "image_basename": IMAGE_BASENAME,
        "image_tag": construct_image_tag({
            "images_infos": [get_image_infos(config["base_image"])],
            "target": config["target"]
        })
    })

def get_config(image: str) -> Config:
    image_infos = get_image_infos(image)
    parsed_image = parse_image_tag(image_infos["image_tag"])
    base_image = get_image_from_infos(parsed_image["images_infos"][0])
    
    return {
        "docker_user": image_infos["image_user"],
        "target": parsed_image["target"],
        "base_image": base_image,
    }
    
def get_target_images(partial_args: dict) -> list[str]:
    target_images = []
    docker_user = partial_args["docker_user"]
    for target in partial_args["target"]:
        for base_image in partial_args["base_image"]:
            target_image = get_target_image({
                "docker_user": docker_user,
                "target": target,
                "base_image": base_image
            })
            if target_image is not None:
                target_images.append(target_image)
    return target_images

def get_dependency(target_image: str) -> str | None:
    config = get_config(target_image)
    base_image = config["base_image"]
    target = config["target"]
    
    if target.endswith("prod"):
        return base_image
    elif target.endswith("dev"):
        return get_target_image({
            **config,
            "target": target.replace("dev", "prod")
        })
        
def get_build_args(target_image: str) -> dict:
    config = get_config(target_image)
    build_args = {}
    build_args["BASE_IMAGE"] = config["base_image"]
    return build_args