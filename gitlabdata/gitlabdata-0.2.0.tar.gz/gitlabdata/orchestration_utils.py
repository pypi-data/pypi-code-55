import json
import logging
import os
import sys
from pathlib import Path
from time import time
from typing import Any, Dict, List, Tuple

import pandas as pd
from snowflake.sqlalchemy import URL as snowflake_URL
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


def postgres_engine_factory(args: Dict[str, str]) -> Engine:
    """
    Create a database engine from a dictionary of database info.
    """

    db_address = args["PG_ADDRESS"]
    db_database = args["PG_DATABASE"]
    db_port = args["PG_PORT"]
    db_username = args["PG_USERNAME"]
    db_password = args["PG_PASSWORD"]

    conn_string = "postgresql://{}:{}@{}:{}/{}".format(
        db_username, db_password, db_address, db_port, db_database
    )

    return create_engine(conn_string, connect_args={"sslcompression": 0})


def snowflake_engine_factory(
    args: Dict[str, str], role: str, schema: str = ""
) -> Engine:
    """
    Create a database engine from a dictionary of database info.
    """

    # Figure out which vars to grab
    role_dict = {
        "SYSADMIN": {
            "USER": "SNOWFLAKE_USER",
            "PASSWORD": "SNOWFLAKE_PASSWORD",
            "ACCOUNT": "SNOWFLAKE_ACCOUNT",
            "DATABASE": "SNOWFLAKE_LOAD_DATABASE",
            "WAREHOUSE": "SNOWFLAKE_LOAD_WAREHOUSE",
            "ROLE": "SYSADMIN",
        },
        "ANALYTICS_LOADER": {
            "USER": "SNOWFLAKE_LOAD_USER",
            "PASSWORD": "SNOWFLAKE_LOAD_PASSWORD",
            "ACCOUNT": "SNOWFLAKE_ACCOUNT",
            "DATABASE": "SNOWFLAKE_TRANSFORM_DATABASE",
            "WAREHOUSE": "SNOWFLAKE_LOAD_WAREHOUSE",
            "ROLE": "LOADER",
        },
        "LOADER": {
            "USER": "SNOWFLAKE_LOAD_USER",
            "PASSWORD": "SNOWFLAKE_LOAD_PASSWORD",
            "ACCOUNT": "SNOWFLAKE_ACCOUNT",
            "DATABASE": "SNOWFLAKE_LOAD_DATABASE",
            "WAREHOUSE": "SNOWFLAKE_LOAD_WAREHOUSE",
            "ROLE": "LOADER",
        },
        "CI_USER": {
            "USER": "SNOWFLAKE_USER",  ## this is the CI User
            "PASSWORD": "SNOWFLAKE_PASSWORD",
            "ACCOUNT": "SNOWFLAKE_ACCOUNT",
            "DATABASE": "SNOWFLAKE_TRANSFORM_DATABASE",
            "WAREHOUSE": "SNOWFLAKE_TRANSFORM_WAREHOUSE",
            "ROLE": "TRANSFORMER",
        },
    }

    vars_dict = role_dict[role]

    conn_string = snowflake_URL(
        user=args[vars_dict["USER"]],
        password=args[vars_dict["PASSWORD"]],
        account=args[vars_dict["ACCOUNT"]],
        database=args[vars_dict["DATABASE"]],
        warehouse=args[vars_dict["WAREHOUSE"]],
        role=vars_dict["ROLE"],  # Don't need to do a lookup on this one
        schema=schema,
    )

    return create_engine(conn_string, connect_args={"sslcompression": 0})


def query_executor(engine: Engine, query: str) -> List[Tuple[Any]]:
    """
    Execute DB queries safely.
    """

    try:
        connection = engine.connect()
        results = connection.execute(query).fetchall()
    finally:
        connection.close()
        engine.dispose()
    return results


def dataframe_enricher(advanced_metadata: bool, raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich a dataframe with metadata and do some cleaning.
    """
    raw_df["_uploaded_at"] = time()  # Add an uploaded_at column

    if advanced_metadata:
        # Add additional metadata from an Airflow scheduler
        # _task_instance is expected to be the task_instance_key_str
        raw_df.loc[:, "_task_instance"] = os.environ["TASK_INSTANCE"]

    # Do some Snowflake-specific sanitation
    enriched_df = (
        raw_df.applymap(  # convert dicts and lists to str to avoid snowflake errors
            lambda x: x if not isinstance(x, (list, dict)) else str(x)
        )
        .applymap(  # shorten strings that are too long
            lambda x: x[:4_194_304] if isinstance(x, str) else x
        )
        .applymap(  # replace tabs with 4 spaces
            lambda x: x.replace("\t", "    ") if isinstance(x, str) else x
        )
    )

    return enriched_df


def dataframe_uploader(
    dataframe: pd.DataFrame,
    engine: Engine,
    table_name: str,
    schema: str = None,
    advanced_metadata: bool = False,
) -> None:
    """
    Upload a dataframe, adding in some metadata and cleaning up along the way.
    """

    dataframe_enricher(advanced_metadata, dataframe).to_sql(
        name=table_name,
        con=engine,
        schema=schema,
        index=False,
        if_exists="append",
        chunksize=10000,
    )


def snowflake_stage_load_copy_remove(
    file: str, stage: str, table_path: str, engine: Engine, type: str = "json"
) -> None:
    """
    Upload file to stage, copy to table, remove file from stage on Snowflake
    """

    put_query = f"put file://{file} @{stage} auto_compress=true;"

    copy_query = f"""copy into {table_path} (jsontext)
                     from @{stage}
                     file_format=(type='{type}'),
                     on_error='skip_file';"""

    remove_query = f"remove @{stage} pattern='.*.{type}.gz'"

    logging.basicConfig(stream=sys.stdout, level=20)

    try:
        connection = engine.connect()

        logging.info(f"Clearing {type} files from stage.")
        remove = connection.execute(remove_query)
        logging.info(remove)

        logging.info("Writing to Snowflake.")
        results = connection.execute(put_query)
        logging.info(results)
    finally:
        connection.close()
        engine.dispose()

    try:
        connection = engine.connect()

        logging.info(f"Copying to Table {table_path}.")
        copy_results = connection.execute(copy_query)
        logging.info(copy_results)

        logging.info(f"Removing {file} from stage.")
        remove = connection.execute(remove_query)
        logging.info(remove)
    finally:
        connection.close()
        engine.dispose()


def push_to_xcom_file(xcom_json: Dict[Any, Any]) -> None:
    """
    Writes the json passed in as a parameter to the file path required by KubernetesPodOperator to make the json an xcom in Airflow.
    Overwrites any data already there.
    This is primarily used to push metrics to prometheus right now.
    """

    xcom_file_name = "/airflow/xcom/return.json"
    Path("/airflow/xcom/").mkdir(parents=True, exist_ok=True)
    with open(xcom_file_name, "w") as xcom_file:
        json.dump(xcom_json, xcom_file)


def append_to_xcom_file(xcom_json: Dict[Any, Any]) -> None:
    """
    Combines the parameter dictionary with any XComs that have already been written by the KubernetesPodOperator.  
    This function is useful because the XComs can be written at any time during the Task run and not be written over.
    """

    existing_json = {}
    try:
        with open("/airflow/xcom/return.json") as json_file:
            existing_json = json.load(json_file)
    except IOError:
        pass  # the file doesn't exist
    except json.JSONDecodeError:
        pass  # the file is likely empty
    push_to_xcom_file({**existing_json, **xcom_json})
