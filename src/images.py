import logging
from importlib import import_module
import os
import random
from config import get_config
from utilities import get_image_infos, parse_image_tag
from dependencies import get_all_target_images

# Set up logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/logs.txt"),
        logging.StreamHandler()
    ]
)

GET_TARGET_IMAGES = {}
GET_BUILD_ARGS = {}
for dockerfile_folder in os.listdir("dockerfiles"):
    module = import_module(f"dockerfiles.{dockerfile_folder}.images")
    image_basename = dockerfile_folder.replace("_", "-")
    GET_BUILD_ARGS[image_basename] = module.get_build_args
    GET_TARGET_IMAGES[image_basename] = module.get_target_images

def get_target_images_from_partials_args(partial_args: dict) -> list[str]:
    """
    Get the target images for a target_image.
    """
    target_images = []
    for get_target_images in GET_TARGET_IMAGES.values():
        target_images.extend(get_target_images(partial_args))
    return target_images

def get_build_args(target_image: str) -> dict:
    """
    Get the build args for a target_image.
    """
    image_infos = get_image_infos(target_image)
    return GET_BUILD_ARGS[image_infos["image_basename"]](target_image)

def get_dockerfile_directory(target_image: str) -> str:
    """
    Get the dockerfile directory for a target_image.
    """
    image_infos = get_image_infos(target_image)
    return f"dockerfiles/{image_infos['image_basename'].replace('-', '_')}"

def build_and_push(target_image: str) -> None:
    image_infos = get_image_infos(target_image)
    image_basename = image_infos["image_basename"]
    target = parse_image_tag(image_infos["image_tag"])["target"]
    logger = logging.getLogger(image_basename)
    file_handler = logging.FileHandler(f"logs/{image_basename.replace('-', '_')}_logs.txt")
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    build_args = get_build_args(target_image)
    joint_build_args = " ".join([f'--build-arg {k}="{v}"' for k, v in build_args.items() if v is not None])
    docker_cmd = f"docker build {joint_build_args} --target {target} -t {target_image} ."
    cmd = f"cd {get_dockerfile_directory(target_image)} && {docker_cmd} && docker push {target_image}"
    logger.info(cmd)
    result = os.system(cmd)
    if result == 0:
        logger.info(f"SUCCESS building and pushing {target_image}")
    else:
        logger.error(f"ERROR occurred while building and pushing {target_image}")

def update_images():
    config = get_config()
    partial_args = config["partial_args"]
    docker_user = partial_args["docker_user"]
    target_images = get_all_target_images(
        config["target_images"] + get_target_images_from_partials_args(partial_args),
        docker_user
    )
    logging.info("Target images:")
    for target_image in target_images:
        logging.info(target_image)
    proceed = input("All these images will be build and pushed.\nProceed? [Y/n]: ")
    if len(proceed) != 0 and proceed.lower() != "y":
        return
    for target_image in target_images:
        build_and_push(target_image)