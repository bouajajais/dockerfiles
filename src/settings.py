CONFIG_FILEPATH = "/app/config/config.json"
DOCKERFILES_FOLDER = "/app/src/dockerfiles"

DEFAULT_CONFIG = {
    "partial_args": {
        "docker_user": "ismailbouajaja",
        "image_type": ["base", "dev-base", "docker-base", "dev-docker-base"],
        "base_image": ["node:16"],
        "docker_version": ["27.3.1"],
        "poetry_version": ["1.8"],
        "python_version": ["3.10", "3.11"],
        "python_type": ["", "slim"],
        "python_os": [""],
        "cuda_version": ["12.4.1", "12.5.1", "12.6.2"],
        "cuda_cudnn": ["", "cudnn"],
        "cuda_type": ["devel"],
        "cuda_os": ["ubuntu22.04"]
    },
    "target_images": [
        "cuda-poetry:12.6.2-cudnn-devel-ubuntu22.04--python-3.11--poetry-1.8--dev"
    ]
}