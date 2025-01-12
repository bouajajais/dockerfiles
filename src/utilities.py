from typing import Literal, TypedDict

Target = Literal["prod", "dev", "alpine-prod", "alpine-dev"]

class ImageInfos(TypedDict):
    image_user: str
    image_basename: str
    image_tag: str
    

class ParsedImageTag(TypedDict):
    target: Target
    images_infos: list[ImageInfos]
    
    
def get_image_infos(image: str) -> ImageInfos:
    image_name, image_tag = image.split(":")
    if "/" in image_name:
        image_user, image_basename = image_name.split("/")
    else:
        image_user = ""
        image_basename = image_name
    return {
        "image_user": image_user,
        "image_basename": image_basename,
        "image_tag": image_tag
    }

def get_image_from_infos(image_infos: ImageInfos) -> str:
    image_user = image_infos["image_user"]
    image_user = "" if len(image_user) == 0 else f"{image_user}/"
    return f"{image_user}{image_infos['image_basename']}:{image_infos['image_tag']}"

def get_image_as_tag_infos(image_as_tag: str) -> ImageInfos:
    try:
        image_user, image_basename, image_tag = image_as_tag.split("__")
    except Exception:
        image_user = ""
        image_basename, image_tag = image_as_tag.split("__")
    return {
        "image_user": image_user,
        "image_basename": image_basename,
        "image_tag": image_tag
    }

def get_image_as_tag_from_infos(image_infos: ImageInfos) -> str:
    image_user = image_infos["image_user"]
    image_user = "" if len(image_user) == 0 else f"{image_user}__"
    return f"{image_user}{image_infos['image_basename']}__{image_infos['image_tag']}"

def parse_image_tag(image_tag: str) -> ParsedImageTag:
    target = "prod"
    if image_tag.endswith("--dev"):
        target = "dev"
    elif image_tag.endswith("--alpine-prod"):
        target = "alpine-prod"
    elif image_tag.endswith("--alpine-dev"):
        target = "alpine-dev"
    
    if target in ["dev", "alpine-prod", "alpine-dev"]:
        image_tag = image_tag[:-len(f"--{target}")]
    
    images_as_tag = image_tag.split("--")
    images_infos = []
    for image_as_tag in images_as_tag:
        image_infos = get_image_as_tag_infos(image_as_tag)
        images_infos.append(image_infos)
        
    return {
        "target": target,
        "images_infos": images_infos
    }

def construct_image_tag(parsed_image_tag: ParsedImageTag) -> str:
    images_as_tag = []
    for image_infos in parsed_image_tag["images_infos"]:
        image_as_tag = get_image_as_tag_from_infos(image_infos)
        images_as_tag.append(image_as_tag)
        
    image_tag = "--".join(images_as_tag)
    if parsed_image_tag["target"] in ["dev", "alpine-prod", "alpine-dev"]:
        image_tag = f"{image_tag}--{parsed_image_tag['target']}"
        
    return image_tag