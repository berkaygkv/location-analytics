import yaml
import os
from pathlib import Path

def load_config():
    ROOT_STRING = os.getcwd().split("geo-clustering-project")[0] + "geo-clustering-project"
    ROOT_DIR = Path(ROOT_STRING)
    config_file_path = Path(ROOT_DIR, "config.yaml")
    with open(config_file_path, "r") as f:
        configs = yaml.safe_load(f)
    return configs

if __name__ == "__main__":
    load_config()
