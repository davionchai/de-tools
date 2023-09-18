import logging

from datetime import datetime
from typing import Any, Union

from structs.pipeline import PipelineStruct
from structs.sourcedb import SourceDbStruct

from utils.connectors import PGConnector

logger: logging = logging.getLogger(__name__)


class ExtractMetadata:
    def __init__(self, source_db: SourceDbStruct, pipeline: PipelineStruct):
        results: tuple[Any, ...] = self.get_select_results(
            source_db=source_db, pipeline=pipeline
        )
        self.source_min, self.source_max = self.parse_source_min_max(results=results)
        self.table_select: str = self.get_table_select(
            source_db=source_db, pipeline=pipeline
        )

    def get_select_results(self, source_db: SourceDbStruct, pipeline: PipelineStruct):
        results: tuple[Any, ...] = tuple()
        if source_db.db_type.lower() == "psql":
            with PGConnector(pg_config=source_db.db_config) as conn:
                with conn.cursor() as cur:
                    logger.info(
                        f"Scanning [{source_db.schema}.{source_db.table}] for max({pipeline.partition_column})..."
                    )
                    query: str = (
                        "select "
                        f"min({pipeline.partition_column}) as source_min"
                        f", max({pipeline.partition_column}) as source_max"
                        ", count(*) as row_count "
                        f"from {source_db.schema}.{source_db.table} "
                    )
                    ## allrun vs upsert mode
                    # if partition_column_type:
                    #     query += f"where {self.partition_column} > "
                    cur.execute(query=query)
                    results = cur.fetchone()

                    ## Assert index and warn
                    # select indexname, indexdef
                    # from pg_indexes
                    # where tablename = 'eorzea_population';
        else:
            err: str = f"Unsupported db type: [{source_db.db_type}]"
            logger.error(err)
            raise ValueError(err)

        return results

    def parse_source_min_max(self, results: tuple[Any, ...]):
        source_min: Union[int, datetime, str] = results[0]
        source_max: Union[int, datetime, str] = results[1]
        if isinstance(source_min, datetime):
            source_min = source_min.isoformat()

        if isinstance(source_max, datetime):
            source_max = source_max.isoformat()

        return source_min, source_max

    def get_table_select(self, source_db: SourceDbStruct, pipeline: PipelineStruct):
        table_select: str = ""
        table_select = f"(select * from {source_db.schema}.{source_db.table} where {pipeline.partition_column} >= "
        if isinstance(self.source_min, int):
            table_select += f"{self.source_min}"
        elif isinstance(self.source_min, str):
            table_select += f"'{self.source_min}'"
        table_select += ") as filter"

        return table_select

    #     # predicates (to be moved to golang)
    #     step_size_factor: int = 1
    #     if isinstance(self.source_min, int) and isinstance(self.source_max, int):
    #         step_size_factor = self.source_max - self.source_min
    #     elif isinstance(self.source_min, datetime) and isinstance(
    #         self.source_max, datetime
    #     ):
    #         datetime_delta: timedelta = self.source_max - self.source_min
    #         match self.datetime_level.lower():
    #             case "weeks":
    #                 step_size_factor = datetime_delta.days * 7
    #             case "days":
    #                 step_size_factor = datetime_delta.days
    #             case "hours":
    #                 step_size_factor = datetime_delta.seconds // 3600
    #             case "minutes":
    #                 step_size_factor = (datetime_delta.seconds // 60) % 60
    #             case "seconds":
    #                 step_size_factor = datetime_delta.seconds
    #             case _:
    #                 err: str = (
    #                     f"Unkown datetime level specified: [{self.datetime_level}]"
    #                 )
    #                 logger.error(err)
    #                 raise ValueError(err)
    #     else:
    #         err: str = f"Unsupported data type found from extracted partitioning col: [{type(self.source_max)}]"
    #         logger.error(err)
    #         raise ValueError(err)

    #     step_size: int = 1
    #     if self.num_partitions or step_size_factor:
    #         step_size = -(-step_size_factor // self.num_partitions)

    #     self.predicates = self.__generate_predicates()

    # def __generate_predicates(self):
    #     # the template
    #     predicate_template = "'{}' <= {} and {} < '{}'"
    #             # Example
    #         # [
    #         #     "'10' <= uid and uid < '2676'",
    #         #     "'2676' <= uid and uid < '5342'",
    #         # ]

    #     # then build the list
    #     predicates = []
    #     for i in range(0, self.num_partitions):
    #         interval_start: Union[int, datetime] = (
    #             self.num_partitions + i * step_size
    #         )
    #         interval_end: Union[int, datetime] = (
    #             self.num_partitions + (i + 1) * step_size
    #         )
    #         if isinstance(interval_start, int) and isinstance(interval_end, int):
    #             predicates.append(
    #                 predicate_template.format(
    #                     interval_start,
    #                     self.partition_column,
    #                     self.partition_column,
    #                     interval_end,
    #                 )
    #             )
    #         elif isinstance(interval_start, datetime) and isinstance(
    #             interval_end, datetime
    #         ):
    #             predicates.append(
    #                 predicate_template.format(
    #                     interval_start.isoformat(),
    #                     self.partition_column,
    #                     self.partition_column,
    #                     interval_end.isoformat(),
    #                 )
    #             )

    #     return predicates
