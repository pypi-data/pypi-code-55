import os
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Optional, TextIO, Union

import pandas as pd
import pyarrow as pa
from pandas.errors import ParserError
from pyarrow import RecordBatchFileWriter

from .config import empty_schema, log
from .df_processor import process_df
from .dp_types import ARROW_MIMETYPE, MIME, DFSchema, Hash


@dataclass
class ImportFileResp:
    cas_ref: Hash
    content_type: MIME
    schema: DFSchema
    file_size: int
    num_rows: int
    num_columns: int


def convert_df_table(df: pd.DataFrame) -> pa.Table:
    process_df(df)
    # NOTE - can pass expected schema and columns for output df here
    table: pa.Table = pa.Table.from_pandas(df, preserve_index=False)
    return table


def convert_csv_table(
    _input: Union[str, TextIO], output: Optional[Union[str, BinaryIO]] = None, ext: str = ".csv"
) -> pa.Table:
    """Convert & return csv/excel file to an arrow table via pandas, optionally writing it disk"""
    df: pd.DataFrame
    # TODO - tie to mimetypes lib
    if ext == ".csv":
        try:
            df = pd.read_csv(_input, engine="c", sep=",")
        except ParserError as e:
            log.warning(f"Error parsing CSV file ({e}), trying python fallback")
            df = pd.read_csv(_input, engine="python", sep=None)
    elif ext == ".xlsx":
        df = pd.read_excel(_input, engine="openpyxl")
    # TODO - remove
    elif ext == ".df.json":
        df = pd.read_json(_input, orient="table")
    else:
        raise NotImplementedError(f"Unknown input type {ext} - supported types are .csv, .xlsx")

    table = convert_df_table(df)
    if output is not None:
        write_table(table, output)

    return table


def import_arrow_file(table: pa.Table, arrow_f_name: str, cas_ref: str = None) -> ImportFileResp:
    file_size = os.path.getsize(arrow_f_name)
    # schema unused atm
    _: pa.Schema = table.schema

    return ImportFileResp(
        cas_ref=cas_ref,
        content_type=ARROW_MIMETYPE,
        schema=empty_schema(),
        file_size=file_size,
        num_rows=table.num_rows,
        num_columns=table.num_columns,
    )


def import_from_csv(in_f_path: Path, arrow_f_name: str) -> pa.Table:
    """
    Import a local file to a local arrow file,
    we use filenames rather than open files as pyarrow docs mention it's more performant
    """
    ext: str = "".join(in_f_path.suffixes)
    # pull imported file and read into an arrow table
    table = convert_csv_table(str(in_f_path), arrow_f_name, ext=ext)
    log.debug(f"Imported CSV file of size {table.shape} with following schema: \n{table.schema}")
    return table


def import_local_file_from_disk(in_f_path: Path, arrow_f_name: str) -> ImportFileResp:
    table = import_from_csv(in_f_path, arrow_f_name)
    return import_arrow_file(table, arrow_f_name)


def write_table(table: pa.Table, sink: Union[str, BinaryIO]):
    """Write an arrow table to a file"""
    writer = RecordBatchFileWriter(sink, table.schema)
    writer.write(table)
    writer.close()
