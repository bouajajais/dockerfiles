import json
import settings
import os

def get_config(
    config_filepath: str = settings.CONFIG_FILEPATH
    ) -> dict:
    try:
        with open(config_filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return settings.DEFAULT_CONFIG

def init_config(
    config_filepath: str = settings.CONFIG_FILEPATH
    ) -> None:
    DEFAULT_CONFIG = settings.DEFAULT_CONFIG
    os.makedirs(os.path.dirname(config_filepath), exist_ok=True)
    with open(config_filepath, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=4)