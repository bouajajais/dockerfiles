import os
from utilities import construct_image_tag, get_image_from_infos, get_image_infos, parse_image_tag
from dockerfiles.node.images import get_target_image as get_target_image_node, get_node_config

CURRENT_DIR = os.path.dirname(__file__)
IMAGE_BASENAME = os.path.basename(CURRENT_DIR).replace("_", "-")
HAS_NO_TAG = True

def get_target_image(config: dict) -> str | None:
    if ("alpine" not in config["create_react_router"] and config["target"] != "prod") \
        or ("alpine" in config["create_react_router"] and config["target"] != "alpine-prod"):
        return None
    
    node_image = f"node:{config['create_react_router']}"
    return get_image_from_infos({
        "image_user": config["docker_user"],
        "image_basename": IMAGE_BASENAME,
        "image_tag": construct_image_tag({
            "images_infos": [get_image_infos(node_image)],
            "target": config["target"]
        })
    })

def get_config(image: str) -> dict:
    image_infos = get_image_infos(image)
    parsed_image = parse_image_tag(image_infos["image_tag"])
    node_tag = parsed_image["images_infos"][0]["image_tag"]
    
    return {
        "docker_user": image_infos["image_user"],
        "target": parsed_image["target"],
        "create_react_router": node_tag
    }
        
def get_target_images(partial_args: dict) -> list[str]:
    target_images = []
    docker_user = partial_args["docker_user"]
    for target in partial_args["target"]:
        for create_react_router in partial_args["create_react_router"]:
            target_image = get_target_image({
                "docker_user": docker_user,
                "target": target,
                "create_react_router": create_react_router
            })
            if target_image is not None:
                target_images.append(target_image)
    return target_images

def get_dependency(target_image: str) -> str:
    config = get_config(target_image)
    return get_target_image_node({
        "docker_user": config["docker_user"],
        "target": config["target"],
        **get_node_config(config["create_react_router"])
    })
    
def get_build_args(target_image: str) -> dict:
    config = get_config(target_image)
    build_args = {}
    build_args["NODE_TAG"] = config["create_react_router"]
    return build_args