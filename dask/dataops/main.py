import dask.dataframe as dd
import pandas as pd
from dask.distributed import Client

if __name__ == "__main__":
    lan_ip: str = ""  # fill in your local ip here, ie 192.168.1.1
    client: Client = Client("tcp://localhost:8786")
    connection_string: str = f"postgresql://admin:password@{lan_ip}:5433/randomizer"

    df_dask: dd.DataFrame = dd.read_sql_table(
        table_name="eorzea_population",
        schema="hydaelyn",
        con=connection_string,
        index_col="uid",
        npartitions=4,
    )

    output_file_path: str = "./output.csv"

    df_local: pd.DataFrame = df_dask.compute()
    df_local.to_csv(output_file_path)

    # df_dask.to_parquet(output_file_path)
    # df_dask.to_csv(output_file_path)
