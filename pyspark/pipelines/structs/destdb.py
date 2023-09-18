import logging
import os

from dataclasses import dataclass, field
from typing import Any, Union
from structs.pgconfig import PGConfigStruct

logger: logging = logging.getLogger(__name__)


@dataclass
class DestDbStruct:
    db_type: str = field(default_factory=lambda: os.environ.get("DEST_DB_TYPE"))
    schema: str = field(default_factory=lambda: os.environ.get("DEST_SCHEMA"))
    table: str = field(default_factory=lambda: os.environ.get("DEST_TABLE"))
    db_config: Union[PGConfigStruct, dict, Any] = None
    min: Union[int, str] = None
    max: Union[int, str] = None
