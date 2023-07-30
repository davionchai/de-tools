import os

from pathlib import Path


from utils.logger import log_setup

if __name__ == "__main__":
    parent_dir: Path = Path(__file__).resolve().parent
    logger = log_setup(
        parent_dir=f"{parent_dir}",
        log_filename=f"{parent_dir.name}",
        logger_level=os.environ.get("LOGGER_LEVEL").upper()
        if os.environ.get("LOGGER_LEVEL")
        else None,
    )
