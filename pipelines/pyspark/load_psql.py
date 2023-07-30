from pathlib import Path
from pyspark.sql import SparkSession, DataFrame
from structs.pgconfig import PGConfigStruct

if __name__ == "__main__":
    parent_dir: Path = Path(__file__).resolve().parent
    csv_path: Path = Path(f"{parent_dir}/data")

    spark: SparkSession = (
        SparkSession.builder.appName("ELT Pipeline")
        .config("spark.jars", "./driver/postgresql-42.6.0.jar")
        .getOrCreate()
    )

    jdbc_config: dict = {
        "user": "admin",
        "password": "password",
        "driver": "org.postgresql.Driver",
    }

    # Read data from PostgreSQL into a DataFrame
    df: DataFrame = spark.read.csv(
        path=csv_path,
        pathGlobFilter="*.csv",
        recursiveFileLookup=True,
        header=True,
        format="csv",
        inferSchema=True,
    )

    df.printSchema()

    # # # Write data to S3 in CSV format
    # # s3_output_path = f"s3a://{s3_bucket}/output_directory"
    # # df.write.option("header", "true").csv(s3_output_path)

    # # Saving data to a JDBC source
    # jdbcDF.write.format("jdbc").option("url", "jdbc:postgresql:dbserver").option(
    #     "dbtable", "schema.tablename"
    # ).option("user", "username").option("password", "password").save()

    # jdbcDF2.write.jdbc(
    #     "jdbc:postgresql:dbserver",
    #     "schema.tablename",
    #     properties={"user": "username", "password": "password"},
    # )

    # # Specifying create table column data types on write
    # jdbcDF.write.option(
    #     "createTableColumnTypes", "name CHAR(64), comments VARCHAR(1024)"
    # ).jdbc(
    #     "jdbc:postgresql:dbserver",
    #     "schema.tablename",
    #     properties={"user": "username", "password": "password"},
    # )

    # Stop the Spark session
    spark.stop()
