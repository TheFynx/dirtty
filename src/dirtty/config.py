import yaml
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def load_config(config_path: Path = Path("config.yaml")):
    logger.info(f"Attempting to load config from {config_path}")
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            logger.info(f"Config loaded successfully: {config}")
            return config
    except FileNotFoundError:
        logger.warning(f"Config file {config_path} not found. Using default configuration.")
        return {}

def save_config(config: dict, config_path: Path = Path("config.yaml")):
    logger.info(f"Saving config to {config_path}")
    with open(config_path, "w") as f:
        yaml.dump(config, f)
    logger.info("Config saved successfully")