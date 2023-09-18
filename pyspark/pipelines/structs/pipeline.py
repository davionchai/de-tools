import logging
import os

from dataclasses import dataclass, field

logger: logging = logging.getLogger(__name__)


@dataclass
class PipelineStruct:
    etl_mode: str = field(default_factory=lambda: os.environ.get("ETL_MODE"))
    partition_column: str = field(
        default_factory=lambda: os.environ.get("PARTITION_COLUMN")
    )
    num_partitions: int = 20  # to be optimized via rownums
    datetime_level: str = "days"
    # predicates: list[str] = field(default_factory=list[str]) # roadmap

    def __post_init__(self):
        objects = ["etl_mode", "partition_column"]
        for obj in objects:
            if getattr(self, obj) is None:
                error_msg: str = f"Missing value for {obj} from environment variable PG_{obj.upper()}"
                logger.error(error_msg)
                raise ValueError(error_msg)
