import logging
import os

from dataclasses import dataclass, field
from typing import Any, Union
from structs.pgconfig import PGConfigStruct

logger: logging = logging.getLogger(__name__)


@dataclass
class SourceDbStruct:
    db_type: str = field(default_factory=lambda: os.environ.get("SOURCE_DB_TYPE"))
    schema: str = field(default_factory=lambda: os.environ.get("SOURCE_SCHEMA"))
    table: str = field(default_factory=lambda: os.environ.get("SOURCE_TABLE"))
    db_config: Union[PGConfigStruct, dict, Any] = None
    min: Union[int, str] = None
    max: Union[int, str] = None
    table_select: str = None
    properties: dict = None
