import os

# ROOT_DIR = "/home/isbou/work/projects/dockerfiles"
ROOT_DIR = "/app"
CONFIG_FILEPATH = os.path.join(ROOT_DIR, "config/config.json")
LOGS_DIR = os.path.join(ROOT_DIR, "data/logs")

DEFAULT_CONFIG = {
    "partial_args": {
        "docker_user": "ismailbouajaja", # "ismailbouajaja"
        "target": ["prod", "dev"], # "prod", "dev"
        "base_image": ["node:16"],
        "docker_tag": ["27.3.1-cli"], # "27.3.1-cli"
        "poetry_version": ["1.8"], # "1.8"
        "python_version": ["3.10", "3.11"], # "3.10", "3.11", "3.12"
        "python_type": ["", "slim"], # "", "slim
        "python_os": [""], # ""
        "cuda_version": ["12.5.1", "12.6.2"], # "12.4.1", "12.5.1", "12.6.2"
        "cuda_cudnn": ["", "cudnn"], # "", "cudnn"
        "cuda_type": ["devel"], # "base", "runtime", "devel"
        "cuda_os": ["ubuntu22.04"] # "ubuntu20.04", "ubuntu22.04", "ubuntu24.04"
    },
    "target_images": [
        "ismailbouajaja/cuda-poetry:nvidia__cuda__12.6.2-cudnn-devel-ubuntu22.04--python__3.12--poetry__1.8--dev",
    ]
}

"""
{
    "partial_args": {
        "docker_user": "ismailbouajaja",
        "target": [
            "prod",
            "dev"
        ],
        "base_image": [],
        "docker_tag": [
            "27.3.1-cli"
        ],
        "poetry_version": [
            "1.8"
        ],
        "python_version": [
            "3.10",
            "3.11"
        ],
        "python_type": [
            "slim"
        ],
        "python_os": [
            ""
        ],
        "cuda_version": [
            "12.5.1",
            "12.6.2"
        ],
        "cuda_cudnn": [
            "cudnn"
        ],
        "cuda_type": [
            "devel"
        ],
        "cuda_os": [
            "ubuntu22.04"
        ]
    },
    "target_images": []
}
"""