import logging
from importlib import import_module
import os
from config import get_config
import settings
from utilities import get_image_infos, parse_image_tag
from dependencies import get_all_target_images

# Set up logging
os.makedirs(settings.LOGS_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(settings.LOGS_DIR, "logs.txt")),
        logging.StreamHandler()
    ]
)

GET_TARGET_IMAGES = {}
GET_BUILD_ARGS = {}
for dockerfile_folder in os.listdir("dockerfiles"):
    module = import_module(f"dockerfiles.{dockerfile_folder}.images")
    image_basename = dockerfile_folder.replace("_", "-")
    GET_TARGET_IMAGES[image_basename] = module.get_target_images
    GET_BUILD_ARGS[image_basename] = module.get_build_args

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

def get_target(target_image: str) -> str:
    """
    Get the target for a target_image.
    """
    return parse_image_tag(target_image)["target"]

def get_dockerfile_directory(target_image: str) -> str:
    """
    Get the dockerfile directory for a target_image.
    """
    image_infos = get_image_infos(target_image)
    return f"dockerfiles/{image_infos['image_basename'].replace('-', '_')}"

def build_and_push(target_image: str) -> None:
    image_infos = get_image_infos(target_image)
    image_basename = image_infos["image_basename"]
    target = get_target(target_image)
    logger = logging.getLogger(image_basename)
    file_handler = logging.FileHandler(os.path.join(settings.LOGS_DIR, f"{image_basename.replace('-', '_')}_logs.txt"))
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    build_args = get_build_args(target_image)
    joint_build_args = " ".join([f'--build-arg {k}="{v}"' for k, v in build_args.items() if v is not None])
    
    cd_cmd = f"cd {get_dockerfile_directory(target_image)}"
    docker_build_cmd = f"sudo docker build {joint_build_args} --target {target} -t {target_image} ."
    docker_push_cmd = f"sudo docker push {target_image}"
    
    cmd = f"{cd_cmd} && {docker_build_cmd} && {docker_push_cmd}"
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
        
def list_images(keywords: list[str]):
    docker_username = get_config()["partial_args"]["docker_user"]
    images = []
    for image_basename in GET_TARGET_IMAGES.keys():
        cmd = f"sudo docker images --format '{{{{.Repository}}}}:{{{{.Tag}}}}' {docker_username}/{image_basename}"
        result = os.popen(cmd).read().strip().split('\n')
        images.extend(result)
    for image in images:
        if all(keyword in image for keyword in keywords):
            print(image)