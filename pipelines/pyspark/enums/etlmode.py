from enum import StrEnum


class EtlMode(StrEnum):
    full_refresh = "full-refresh"
    upsert = "upsert"
    append = "append"
