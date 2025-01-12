import os
from utilities import construct_image_tag, get_image_from_infos, get_image_infos, parse_image_tag
from dockerfiles.poetry.images import get_target_image as get_target_image_node, get_python_config

CURRENT_DIR = os.path.dirname(__file__)
IMAGE_BASENAME = os.path.basename(CURRENT_DIR).replace("_", "-")
HAS_NO_TAG = True

def get_target_image(config: dict) -> str | None:
    if ("alpine" not in config["poetry_init_python_tag"] and config["target"] != "prod") \
        or ("alpine" in config["poetry_init_python_tag"] and config["target"] != "alpine-prod"):
        return None
    
    if config["poetry_init_poetry_version"] == "" or config["poetry_init_python_tag"] == "":
        return None
    
    poetry_image = f"poetry:{config['poetry_init_poetry_version']}"
    python_image = f"python:{config['poetry_init_python_tag']}"
    return get_image_from_infos({
        "image_user": config["docker_user"],
        "image_basename": IMAGE_BASENAME,
        "image_tag": construct_image_tag({
            "images_infos": [get_image_infos(poetry_image), get_image_infos(python_image)],
            "target": config["target"]
        })
    })

def get_config(image: str) -> dict:
    image_infos = get_image_infos(image)
    parsed_image = parse_image_tag(image_infos["image_tag"])
    poetry_version = parsed_image["images_infos"][0]["image_tag"]
    python_tag = parsed_image["images_infos"][1]["image_tag"]
    
    return {
        "docker_user": image_infos["image_user"],
        "target": parsed_image["target"],
        "poetry_init_poetry_version": poetry_version,
        "poetry_init_python_tag": python_tag
    }
        
def get_target_images(partial_args: dict) -> list[str]:
    target_images = []
    docker_user = partial_args["docker_user"]
    for target in partial_args["target"]:
        for poetry_init_poetry_version in partial_args["poetry_init_poetry_version"]:
            for poetry_init_python_tag in partial_args["poetry_init_python_tag"]:
                target_image = get_target_image({
                    "docker_user": docker_user,
                    "target": target,
                    "poetry_init_poetry_version": poetry_init_poetry_version,
                    "poetry_init_python_tag": poetry_init_python_tag
                })
                if target_image is not None:
                    target_images.append(target_image)
    return target_images

def get_dependency(target_image: str) -> str:
    config = get_config(target_image)
    return get_target_image_node({
        "docker_user": config["docker_user"],
        "target": config["target"],
        "poetry_version": config["poetry_init_poetry_version"],
        **get_python_config(config["poetry_init_python_tag"])
    })
    
def get_build_args(target_image: str) -> dict:
    config = get_config(target_image)
    build_args = {}
    build_args["POETRY_VERSION"] = config["poetry_init_poetry_version"]
    build_args["PYTHON_TAG"] = config["poetry_init_python_tag"]
    return build_args