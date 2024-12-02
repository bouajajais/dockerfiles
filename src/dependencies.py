from importlib import import_module
import os
from utilities import get_image_infos

GET_DEPENDENCY = {}
for dockerfile_folder in os.listdir("dockerfiles"):
    module = import_module(f"dockerfiles.{dockerfile_folder}.images")
    image_basename = dockerfile_folder.replace("_", "-")
    GET_DEPENDENCY[image_basename] = module.get_dependency

def has_dependency(target_image: str, docker_user: str) -> bool:
    """
    Check if a target_image has a dependency.
    """
    return target_image.startswith(docker_user)

def get_dependency(target_image: str) -> str:
    """
    Get the dependency for a target_image.
    """
    image_infos = get_image_infos(target_image)
    return GET_DEPENDENCY[image_infos["image_basename"]](target_image)

def resolve_dependencies(target_image: str, resolved: set, result: list, docker_user: str):
    """
    Recursively resolve dependencies for a target_image.
    """
    if target_image in resolved:
        return  # Avoid re-processing already resolved targets
    
    if not has_dependency(target_image, docker_user):  # Check if the target_image has a dependency
        return
    
    dependency = get_dependency(target_image)
    resolve_dependencies(dependency, resolved, result, docker_user)

    # Add the target_image to the result list and mark it as resolved
    result.append(target_image)
    resolved.add(target_image)

def get_all_target_images(target_images: list[str], docker_user: str) -> list[str]:
    """
    Build the final_targets list with dependencies resolved.
    """
    resolved = set()  # Set to keep track of resolved target_images
    final_targets = []  # List to store the final ordered target_images
    
    for target_image in target_images:
        resolve_dependencies(target_image, resolved, final_targets, docker_user)
    
    return final_targets

if __name__ == "__main__":
    import settings
    
    target_images = get_all_target_images(settings.DEFAULT_CONFIG["target_images"], settings.DEFAULT_CONFIG["partial_args"]["docker_user"])
    for target_image in target_images[::-1]:
        print(target_image)