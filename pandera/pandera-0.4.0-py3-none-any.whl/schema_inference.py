"""Module for inferring dataframe/series schema."""

from typing import Union

import pandas as pd

from .schemas import DataFrameSchema, SeriesSchema
from .schema_components import Column, Index, MultiIndex
from .schema_statistics import (
    infer_dataframe_statistics,
    infer_series_statistics,
    parse_check_statistics,
)


def infer_schema(
        pandas_obj: Union[pd.DataFrame, pd.Series]
) -> Union[DataFrameSchema, SeriesSchema]:
    """Infer schema for pandas DataFrame or Series object.

    :param pandas_obj: DataFrame or Series object to infer.
    :returns: DataFrameSchema or SeriesSchema
    :raises: TypeError if pandas_obj is not expected type.
    """
    if isinstance(pandas_obj, pd.DataFrame):
        return infer_dataframe_schema(pandas_obj)
    elif isinstance(pandas_obj, pd.Series):
        return infer_series_schema(pandas_obj)
    else:
        raise TypeError(
            "pandas_obj type not recognized. Expected a pandas DataFrame or "
            "Series, found %s" % type(pandas_obj)
        )


def _create_index(index_statistics):
    index = [
        Index(
            properties["pandas_dtype"],
            checks=parse_check_statistics(properties["checks"]),
            nullable=properties["nullable"],
            name=properties["name"],
        )
        for properties in index_statistics
    ]
    if len(index) == 1:
        index = index[0]  # type: ignore
    else:
        index = MultiIndex(index)  # type: ignore

    return index


def infer_dataframe_schema(df: pd.DataFrame) -> DataFrameSchema:
    """Infer a DataFrameSchema from a pandas DataFrame.

    :param df: DataFrame object to infer.
    :returns: DataFrameSchema
    """
    df_statistics = infer_dataframe_statistics(df)

    schema = DataFrameSchema(
        columns={
            colname: Column(
                properties["pandas_dtype"],
                checks=parse_check_statistics(properties["checks"]),
                nullable=properties["nullable"],
            )
            for colname, properties in df_statistics["columns"].items()
        },
        index=_create_index(df_statistics["index"]),
        coerce=True,
    )
    schema._is_inferred = True  # pylint: disable=protected-access
    return schema


def infer_series_schema(series) -> SeriesSchema:
    """Infer a SeriesSchema from a pandas DataFrame.

    :param series: Series object to infer.
    :returns: SeriesSchema
    """
    series_statistics = infer_series_statistics(series)
    schema = SeriesSchema(
        pandas_dtype=series_statistics["pandas_dtype"],
        checks=parse_check_statistics(series_statistics["checks"]),
        nullable=series_statistics["nullable"],
        name=series_statistics["name"],
        coerce=True,
    )
    schema._is_inferred = True  # pylint: disable=protected-access
    return schema
