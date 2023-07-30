import os

from datetime import datetime
from pathlib import Path
from pyspark.sql import SparkSession, DataFrame

from enums.datetimefmt import DatetimeLevel

from structs.pgconfig import PGConfigStruct
from structs.pipeline import PipelineStruct
from structs.sourcedb import SourceDbStruct

from utils.janitor import init_path
from utils.logger import log_setup
from utils.metadata import ExtractMetadata


def main():
    parent_dir: Path = Path(__file__).resolve().parent
    output_path: str = Path(f"{parent_dir}/data")
    init_path(output_path=output_path)
    pipeline: PipelineStruct = PipelineStruct(
        etl_mode="allrun",
        partition_column="created_at",
        num_partitions=10,
        datetime_level=DatetimeLevel.hours,  # ignored if partition_column is not datetime
    )
    pg_config: PGConfigStruct = PGConfigStruct()
    source_db: SourceDbStruct = SourceDbStruct(
        db_type="psql",
        schema="hydaelyn",
        table="eorzea_population",
        db_config=pg_config,
    )
    extract_metadata: ExtractMetadata = ExtractMetadata(
        source_db=source_db, pipeline=pipeline
    )

    source_db.min = extract_metadata.source_min
    source_db.max = extract_metadata.source_max
    source_db.table_select = extract_metadata.table_select

    spark: SparkSession = (
        SparkSession.builder.appName("ELT Pipeline")
        .config("spark.jars", f"{parent_dir}/drivers/postgresql-42.6.0.jar")
        .getOrCreate()
    )

    df: DataFrame = (
        spark.read.format("jdbc")
        .option("driver", pg_config.driver)
        .option("url", pg_config.url)
        .option("dbtable", source_db.table_select)
        .option("user", pg_config.user)
        .option("password", pg_config.password)
        .option("partitionColumn", pipeline.partition_column)
        .option("lowerBound", source_db.min)
        .option("upperBound", source_db.max)
        .option("numPartitions", pipeline.num_partitions)
        .load()
    )

    logger.info(df.explain())

    file_date_partition: str = datetime.now().strftime("%Y%m%dT%H%M%S")
    csv_path: str = f"file://{output_path}/eorzea_population/{file_date_partition}"
    df.write.csv(
        path=csv_path,
        header=True,
        sep=",",
        encoding="UTF-8",
        quote='"',
        ignoreLeadingWhiteSpace=False,
        ignoreTrailingWhiteSpace=False,
        dateFormat="yyyy-MM-dd",
        timestampFormat="yyyy-MM-dd'T'HH:mm:ss[.SSS]",
        emptyValue="",
    )

    # # Set S3 bucket and credentials
    # s3_bucket: str = "de-pyspark-sandbox"
    # # aws_access_key_id = ""
    # # aws_secret_access_key = ""
    # # aws_region = ""
    # # Write data to S3 in CSV format
    # s3_output_path = f"s3a://{s3_bucket}/output_directory"
    # df.write.option("header", "true").csv(s3_output_path)

    spark.stop()


if __name__ == "__main__":
    parent_dir: Path = Path(__file__).resolve().parent
    logger = log_setup(
        parent_dir=f"{parent_dir}",
        log_filename=f"{parent_dir.name}",
        logger_level=os.environ.get("LOGGER_LEVEL").upper()
        if os.environ.get("LOGGER_LEVEL")
        else None,
    )
    main()
