import os
from utilities import construct_image_tag, get_image_from_infos, get_image_infos, parse_image_tag
from dockerfiles.uv.images import get_target_image as get_target_image_node, get_uv_config

CURRENT_DIR = os.path.dirname(__file__)
IMAGE_BASENAME = os.path.basename(CURRENT_DIR).replace("_", "-")
HAS_NO_TAG = True

def get_target_image(config: dict) -> str | None:
    if ("alpine" not in config["uv_init"] and config["target"] != "prod") \
        or ("alpine" in config["uv_init"] and config["target"] != "alpine-prod"):
        return None
    
    uv_image = f"uv:{config['uv_init']}"
    return get_image_from_infos({
        "image_user": config["docker_user"],
        "image_basename": IMAGE_BASENAME,
        "image_tag": construct_image_tag({
            "images_infos": [get_image_infos(uv_image)],
            "target": config["target"]
        })
    })

def get_config(image: str) -> dict:
    image_infos = get_image_infos(image)
    parsed_image = parse_image_tag(image_infos["image_tag"])
    uv_tag = parsed_image["images_infos"][0]["image_tag"]
    
    return {
        "docker_user": image_infos["image_user"],
        "target": parsed_image["target"],
        "uv_init": uv_tag
    }
        
def get_target_images(partial_args: dict) -> list[str]:
    target_images = []
    docker_user = partial_args["docker_user"]
    for target in partial_args["target"]:
        for uv_init in partial_args["uv_init"]:
            target_image = get_target_image({
                "docker_user": docker_user,
                "target": target,
                "uv_init": uv_init
            })
            if target_image is not None:
                target_images.append(target_image)
    return target_images

def get_dependency(target_image: str) -> str:
    config = get_config(target_image)
    return get_target_image_node({
        "docker_user": config["docker_user"],
        "target": config["target"],
        **get_uv_config(config["uv_init"])
    })
    
def get_build_args(target_image: str) -> dict:
    config = get_config(target_image)
    build_args = {}
    build_args["UV_TAG"] = config["uv_init"]
    return build_args