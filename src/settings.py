import os

# ROOT_DIR = "/home/isbou/work/projects/dockerfiles"
ROOT_DIR = "/app"
CONFIG_FILEPATH = os.path.join(ROOT_DIR, "config/config.json")
LOGS_DIR = os.path.join(ROOT_DIR, "data/logs")

DEFAULT_CONFIG = {
    "partial_args": {
        "docker_user": "ismailbouajaja", # "ismailbouajaja"
        "target": ["prod", "dev"], # "prod", "dev"
        "base_image": [],
        "docker_tag": ["27.3.1-cli"], # "27.3.1-cli"
        "poetry_version": ["1.8"], # "1.8"
        "python_version": ["3.10", "3.11", "3.12"], # "3.10", "3.11", "3.12"
        "python_type": ["", "slim"], # "", "slim
        "python_os": [""], # ""
        "cuda_version": ["12.4.1", "12.5.1", "12.6.2"], # "12.4.1", "12.5.1", "12.6.2"
        "cuda_cudnn": ["", "cudnn"], # "", "cudnn"
        "cuda_type": ["devel"], # "base", "runtime", "devel"
        "cuda_os": ["ubuntu22.04"], # "ubuntu20.04", "ubuntu22.04", "ubuntu24.04"
        "nodejs_version": ["22"], # "22"
        "nodejs_os": ["bullseye"], # "bullseye"
        "nodejs_type": ["slim"], # "slim
    },
    "target_images": []
}