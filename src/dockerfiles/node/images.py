import os
from utilities import construct_image_tag, get_image_from_infos, get_image_infos, parse_image_tag
from dockerfiles.base.images import get_target_image as get_target_image_base

CURRENT_DIR = os.path.dirname(__file__)
IMAGE_BASENAME = os.path.basename(CURRENT_DIR).replace("_", "-")

def get_node_tag(config: dict) -> str:
    node_version = config["node_version"]
    node_os = "" if config["node_os"] == "" else f"-{config['node_os']}"
    node_type = "" if config["node_type"] == "" else f"-{config['node_type']}"
    return f"{node_version}{node_os}{node_type}"

def get_node_config(node_tag: str) -> dict:
    node_tag_details = node_tag.split("-")
    node_version = node_tag_details[0]
    
    node_type = ""
    if "slim" in node_tag_details:
        node_type = "slim"
    
    node_os = ""
    if len(node_tag_details) > 0 and node_tag_details[1] not in (node_version, node_type):
        node_os = node_tag_details[1]
    
    return {
        "node_version": node_version,
        "node_os": node_os,
        "node_type": node_type,
    }

def get_target_image(config: dict) -> str | None:
    if config["target"] not in ("prod", "dev"):
        return None
    
    node_image = f"node:{get_node_tag(config)}"
    return get_image_from_infos({
        "image_user": config["docker_user"],
        "image_basename": IMAGE_BASENAME,
        "image_tag": construct_image_tag(
            [get_image_infos(node_image)],
            config["target"]
        )
    })

def get_config(image: str) -> dict:
    image_infos = get_image_infos(image)
    parsed_image = parse_image_tag(image_infos["image_tag"])
    node_tag = parsed_image["images_infos"][0]["image_tag"]
    
    return {
        "docker_user": image_infos["image_user"],
        "target": parsed_image["target"],
        **get_node_config(node_tag)
    }
        
def get_target_images(partial_args: dict) -> list[str]:
    target_images = []
    docker_user = partial_args["docker_user"]
    for target in partial_args["target"]:
        for node_version in partial_args["node_version"]:
            for node_os in partial_args["node_os"]:
                for node_type in partial_args["node_type"]:
                    target_image = get_target_image({
                        "docker_user": docker_user,
                        "target": target,
                        "node_version": node_version,
                        "node_os": node_os,
                        "node_type": node_type
                    })
                    if target_image is not None:
                        target_images.append(target_image)
    return target_images

def get_dependency(target_image: str) -> str:
    config = get_config(target_image)
    return get_target_image_base({
        "docker_user": config["docker_user"],
        "target": config["target"],
        "base_image": f"node:{get_node_tag(config)}"
    })
    
def get_build_args(target_image: str) -> dict:
    config = get_config(target_image)
    build_args = {}
    build_args["NODE_TAG"] = get_node_tag(config)
    return build_args