import os
from utilities import construct_image_tag, get_image_from_infos, get_image_infos, parse_image_tag
from dockerfiles.base.images import get_target_image as get_target_image_base

CURRENT_DIR = os.path.dirname(__file__)
IMAGE_BASENAME = os.path.basename(CURRENT_DIR).replace("_", "-")
HAS_NO_TAG = False

def get_uv_tag(config: dict) -> str:
    setup = []
    if config["uv_version"] != "":
        setup.append(config["uv_version"])
    if config["python_version"] != "":
        setup.append(f"python{config['python_version']}")
    if config["uv_os"] != "":
        setup.append(config["uv_os"])
    if config["uv_type"] != "":
        setup.append(config["uv_type"])
    return "-".join(setup)

def get_uv_config(uv_tag: str) -> dict:
    uv_config = {
        "uv_version": "",
        "python_version": "",
        "uv_os": "",
        "uv_type": ""
    }
    uv_tag_details = uv_tag.split("-")
    for detail in uv_tag_details:
        if all(char.isdigit() for char in detail.split(".")):
            uv_config["uv_version"] = detail
        elif "python" in detail:
            uv_config["python_version"] = detail.replace("python", "")
        elif uv_config["uv_os"] == "":
            uv_config["uv_os"] = detail
        else:
            uv_config["uv_type"] = detail
    return uv_config

def get_target_image(config: dict) -> str | None:
    if ("alpine" not in config["uv_os"] and config["target"] not in ("prod", "dev")) \
        or ("alpine" in config["uv_os"] and config["target"] not in ("alpine-prod", "alpine-dev")):
        return None

    if config["uv_os"] in ["", "alpine"] and config["uv_type"] != "":
        return None
    
    uv_image = f"ghcr.io/astral-sh/uv:{get_uv_tag(config)}"
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
        **get_uv_config(uv_tag)
    }
        
def get_target_images(partial_args: dict) -> list[str]:
    target_images = []
    docker_user = partial_args["docker_user"]
    for target in partial_args["target"]:
        for uv_version in partial_args["uv_version"]:
            for python_version in partial_args["python_version"]:
                for uv_os in partial_args["uv_os"]:
                    for uv_type in partial_args["uv_type"]:
                        target_image = get_target_image({
                            "docker_user": docker_user,
                            "target": target,
                            "uv_version": uv_version,
                            "python_version": python_version,
                            "uv_os": uv_os,
                            "uv_type": uv_type
                        })
                        if target_image is not None:
                            target_images.append(target_image)
    return target_images

def get_dependency(target_image: str) -> str:
    config = get_config(target_image)
    return get_target_image_base({
        "docker_user": config["docker_user"],
        "target": config["target"],
        "base_image": f"ghcr.io/astral-sh/uv:{get_uv_tag(config)}"
    })
    
def get_build_args(target_image: str) -> dict:
    config = get_config(target_image)
    build_args = {}
    build_args["UV_TAG"] = get_uv_tag(config)
    return build_args