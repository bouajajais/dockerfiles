import os
import settings
from config import get_config

config = get_config()

target_images = config["target_images"]
partial_args = config["partial_args"]



    
def build(target_image: str) -> None:
    config = get_config(target_image)
    build_args = {}
    build_args["BASE_IMAGE"] = config.get("base_image")
    joint_build_args = " ".join([f'--build-arg {k}="{v}"' for k, v in build_args.items() if v is not None])
    docker_cmd = f"docker build {joint_build_args} --target {config['target']} -t {target_image} ."
    os.system(f"cd {CURRENT_DIR} && {docker_cmd}")






def update_images():
    pass