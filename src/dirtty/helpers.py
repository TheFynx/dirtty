import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def setup_logging(log_level: str) -> None:
    if isinstance(log_level, int):
        log_level = logging.getLevelName(log_level)

    log_level = log_level.upper()
    numeric_level = getattr(logging, log_level, None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')

    log_dir = Path.home() / ".dirtty" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "dirtty.log"

    logging.basicConfig(
        filename=str(log_file),
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger.info(f"Logging setup complete. Log level: {log_level}")
    logger.info(f"Log file location: {log_file}")

def ensure_directory(directory: str) -> Path:
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Ensured directory exists: {path}")
    return path

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')