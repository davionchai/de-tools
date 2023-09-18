import logging
import sys

from datetime import datetime
from functools import wraps
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Optional, Union


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if hasattr(record, "name_override"):
            record.funcName = record.name_override
        return super().format(record)


def log_setup(
    parent_dir: Union[Path, str],
    log_filename: str,
    logger_level: str,
    log_stdout: bool = True,
    log_name: Optional[str] = None,
):
    _parent_dir: Path = Path(parent_dir)
    _logs_path: Path = Path(f"{_parent_dir}/logs/")
    if not _logs_path.exists():
        _logs_path.mkdir(parents=True, exist_ok=True)
    _log_filename_path: Path = Path(f"{_logs_path}/{log_filename}.log")

    # Setting log format
    log_format: str = "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(funcName)s - %(message)s"
    formatter = CustomFormatter(fmt=log_format, datefmt="%Y-%m-%d %I:%M:%S %p")

    # Start setup of logger
    logger = logging.getLogger(log_name) if log_name else logging.getLogger()

    available_logger_level: list[str] = [
        "NOTSET",
        "DEBUG",
        "INFO",
        "WARN",
        "ERROR",
        "CRITICAL",
    ]
    logger_level = logger_level if logger_level in available_logger_level else "INFO"

    logger.setLevel(logger_level)

    # Create Time Rotating File handler with logging level at INFO
    handler = TimedRotatingFileHandler(
        _log_filename_path, when="midnight", backupCount=10
    )
    handler.setFormatter(formatter)
    handler.suffix = "_%Y-%m-%d_%H%M%S.log"
    logger.addHandler(handler)

    if log_stdout:
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logger_level)
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger


def log_time(logger, msg=""):
    def real_decorator(func):
        @wraps(func)
        def log_wrapper(*args, **kwargs):
            logger.info(f"{msg}")
            start = datetime.now()

            result = func(*args, **kwargs)
            duration = datetime.now() - start
            logger.info(f"Duration for {msg}: {duration}")

            return result

        return log_wrapper

    return real_decorator
