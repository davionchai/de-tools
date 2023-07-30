import logging
import psycopg2

from typing import Union
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from structs.pgconfig import PGConfigStruct

logger: logging = logging.getLogger(__name__)


class PGConnector:
    def __init__(self, pg_config: Union[PGConfigStruct, dict]):
        _pg_config: dict = {}
        if isinstance(pg_config, PGConfigStruct):
            _pg_config = {
                "dbname": pg_config.dbname,
                "user": pg_config.user,
                "password": pg_config.password,
                "host": pg_config.host,
                "port": pg_config.port,
            }
        elif isinstance(pg_config, dict):
            _pg_config = {
                "dbname": pg_config.get("dbname"),
                "user": pg_config.get("user"),
                "password": pg_config.get("password"),
                "host": pg_config.get("host"),
                "port": pg_config.get("port"),
            }
        else:
            err: str = f"None standard config provided: [{pg_config}]"
            logger.error(err)
            raise err

        try:
            self.conn: psycopg2.connection = psycopg2.connect(**_pg_config)
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            logger.info(
                f"Successfully connected to postgresdb [{_pg_config.get('host')}/{_pg_config.get('port')}]!"
            )
        except Exception as e:
            logger.error(e)
            logger.error(
                "Cannot connect to postgresdb with hostname: "
                f"[{_pg_config.get('host')}/{_pg_config.get('port')}]! Exiting script."
            )
            raise e

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.conn.close()
