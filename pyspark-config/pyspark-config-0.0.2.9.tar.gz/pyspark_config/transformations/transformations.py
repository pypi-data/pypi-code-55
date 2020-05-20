"""Transformation types for PySpark-config configuration file."""

from typing import List, Any, Callable
from dataclasses import dataclass
import pyspark
import pyspark.sql.functions as F
from pyspark.sql.types import StringType
from pyspark.sql import DataFrame, Window

from pyspark_config.yamlConfig.config import dataclass_json


@dataclass_json
@dataclass
class Transformation:
    """Transformation

    """
    type: str = None

    def transform(self, df):
        raise NotImplementedError("Each transformation must have a transform method.")


#@dataclass_json
#@dataclass
#class Base64(Transformation):
#    type = "Base64"
#    col: str = None
#    colName: str = None
#    isEncryped : bool =None

#    def transform(self, df, jvm) -> DataFrame:
#        col_=df._jdf.col(self.col)
#        isEncrypted_=jvm.scala.Some(self.isEncryped)
#        base64CaseClass = jvm.transformation.transformations.Base64(self.colName, isEncrypted_)
#        result = jvm.transformation.transformations.column.Base64Imp.transformation(base64CaseClass, col_)
#        if result.isLeft():
#            raise Exception(result)
#        else:
#            return result


@dataclass_json
@dataclass
class Cast(Transformation):
    """
    Casts column DataType.

    Args:
    ------
    col: String. Column considered to cast.
    castedCol: String. Column name of the casted column.
    fromType: String. DataType of 'col'.
    toType: String. DataType of 'castedCol'.

    ---- Example: ----
    Cast('age', 'ages', 'int', 'string').transform(df).collect()
    [Row(age=2), Row(ages=u'2')]

    """
    type = "Cast"
    col: str = None
    castedCol: str = None
    fromType: str = None
    toType: str = None

    def transform(self, df) -> DataFrame:
        # TODO ALL TYPES MUST BE CONSIDERED
        casted_column = df[self.col].cast(self.toType)
        return df.withColumn(self.castedCol, casted_column)


@dataclass_json
@dataclass
class CollectList(Transformation):
    """
    Generates list inside columns.

    Args:
    ------
    orderBy: List[String].
    groupBy: List[String].
    col: List[String].

    ---- Example: ----
    CollectList(['country'], ['country'], ['city']).transform(df).show()
        +-------------+--------------------------+
        |country      |city_list                 |
        +-------------+--------------------------+
        |Germany      |[Aachen, Berlin, Hamburg ]|
        |Spain        |[Bilbao, Madrid, Seville] |
        |United States|[New York, Washington]    |
        +-------------+--------------------------+

    """
    type = "CollectList"
    orderBy: List[str] = None
    groupBy: List[str] = None
    cols: List[str] = None

    def transform(self, df) -> DataFrame:
        w = Window.partitionBy(self.groupBy).orderBy(self.orderBy)

        def columnwise(df, column):
            new_column_name = '{}_list'.format(column)
            return df.withColumn(
                new_column_name,
                F.collect_list(df[column]).over(w)
            )

        def columnwise_(column):
            new_column_name = '{}_list'.format(column)
            return F.max(new_column_name).alias(new_column_name)

        column_list_ = [columnwise_(column) for column in self.cols]
        for column in self.cols:
            df = columnwise(df, column)
        return df.groupby(self.groupBy).agg(*column_list_)


@dataclass_json
@dataclass
class Concatenate(Transformation):
    """
    Creates a column concatenating the indicated columns
    with a delimiter (Default: ""). Number of columns to
    concatenate is undetermined.

    Args:
    ------
    cols: List[String]. Columns to concatenate. Column type must be a string.
    name: String. Column name of the concatenated column.
    delimiter: String. Specifies the boundary between separate columns in
        the concatenated sequence.

    ---- Example: ----
    Concatenate(['name', 'surname'], 'concat', '-').transform(df).collect()
    [Row(name= u'Max', name=u'Muster', concat='uMax-Muster')]
    Concatenate(['name', 'surname'], 'concat').transform(df).collect()
    [Row(name= 'uMax', name=u'Muster', concat=u'MaxMuster')]
    """
    type = "Concatenate"
    cols: List[str] = None
    name: str = None
    delimiter: str = ""

    def transform(self, df) -> DataFrame:
        func: Callable[[Any], str] = lambda cols: \
            self.delimiter.join([x if x is not None else "" for x in cols])
        concat_udf = F.udf(func, StringType())
        return df.withColumn(self.name, concat_udf(F.array(*self.cols)))


@dataclass_json
@dataclass
class DayOfMonth(Transformation):
    """
    Extract the day of month of a given date as integer.

    Args:
    ------
    date: String. Column with DateType where month to extract from.
    colName: String. Column name of day of month content.

    ---- Example: ----
    df = spark.createDataFrame([('2015-04-08',)], ['dt'])
    DayOfMonth('dt', 'dayOfMonth').transform(df).collect()
    [Row(dt='2015-04-08', dayOfMonth=7)]
    """
    type = "Month"
    date: str = None
    colName: str = None

    def transform(self, df) -> DataFrame:
        return df.withColumn(colName=self.colName, col=(F.dayofmonth(self.date)-1))


@dataclass_json
@dataclass
class DayOfYear(Transformation):
    """
    Extract the day of year of a given date as integer.

    Args:
    ------
    date: String. Column with DateType where month to extract from.
    colName: String. Column name of day of year content.

    ---- Example: ----
    df = spark.createDataFrame([('2015-04-08',)], ['dt'])
    DayOfYear('dt', 'dayOfYear').transform(df).collect()
    [Row(dt='2015-04-08', dayOfYear=97)]
    """
    type = "DayOfYear"
    date: str = None
    colName: str = None

    def transform(self, df) -> DataFrame:
        return df.withColumn(colName=self.colName, col=(F.dayofyear(self.date)-1))


@dataclass_json
@dataclass
class DayOfWeek(Transformation):
    """
    Extract the day of week of a given date as integer.

    Args:
    ------
    date: String. Column with DateType where day of week to extract from.
    colName: String. Column name of day of week content.

    ---- Example: ----
    df = spark.createDataFrame([('2015-04-08',)], ['dt'])
    DayOfWeek('dt', 'dayOfWeek').transform(df).collect()
    [Row(dt='2015-04-08', dayOfWeek=3)]
    """
    type = "DayOfWeek"
    date: str = None
    colName: str = None

    def transform(self, df) -> DataFrame:
        return df.withColumn(colName=self.colName, col=(F.dayofweek(self.date)-1))



@dataclass_json
@dataclass
class Filter(Transformation):
    """Filters rows using the given condition.

    :func:`where` is an alias for :func:`filter`.

    Args:
    ------
    condition: String. A string of SQL expression.

    ---- Example: ----
    Filter('age > 3').transform(df).collect()
    [Row(age=5, name=u'Bob')]
    Filter('age == 2').transform(df).collect()
    [Row(age=2, name=u'Alice')]
    """
    type = "Filter"
    sql_condition: str = None

    def transform(self, df) -> DataFrame:
        return df.filter(self.sql_condition)


@dataclass_json
@dataclass
class FilterByList(Transformation):
    """Filters column by a list of values.

    :func:`where` is an alias for :func:`filter`.

    Args:
    ------
    col: String. Column considered in filter.
    values: List[String]. Values which should remain
        in the given column 'col'.

    ---- Example: ----
    FilterByList('name', ['Bob', 'Max']).transform(df).collect()
    [Row(name=u'Bob'), Row(name=u'Max')]
    FilterByList('name', ['Bob']).transform(df).collect()
    [Row(name=u'Bob')]

    """
    type = "FilterByList"
    col: str = None
    values: List[str] = None

    def transform(self, df) -> DataFrame:
        return df.where((F.col(self.col).isin(self.values)))


@dataclass_json
@dataclass
class Aggregation:
    func: str = None
    cols: List[str] = None


@dataclass_json
@dataclass
class GroupBy(Transformation):
    """"
    Groups the :class:`DataFrame` using the specified columns,
    so we can run aggregation on them. See :class:`GroupedData`
    for all the available aggregate functions.

    :func:`groupby` is an alias for :func:`groupBy`.

    Args:
    ------
    :param groupBy: list of columns to group by.
        Each element should be a column name (string) or an expression (:class:`Column`).
    :param sumBy: list of columns to sum by groups.
        Each element should be a column name (string) or an expression (:class:`Column`).
    :param countBy: list of columns to count by groups.
        Each element should be a column name (string) or an expression (:class:`Column`).

    ---- Example: ----
    df.groupBy().avg().collect()
    [Row(avg(age)=3.5)]
    sorted(df.groupBy('name').agg({'age': 'mean'}).collect())
    [Row(name=u'Alice', avg(age)=2.0), Row(name=u'Bob', avg(age)=5.0)]
    sorted(df.groupBy(df.name).avg().collect())
    [Row(name=u'Alice', avg(age)=2.0), Row(name=u'Bob', avg(age)=5.0)]
    sorted(df.groupBy(['name', df.age]).count().collect())
    [Row(name=u'Alice', age=2, count=1), Row(name=u'Bob', age=5, count=1)]
    """
    type = "GroupBy"
    groupBy: List[str] = None
    aggregations: List[Aggregation] = None

    def transform(self, df) -> DataFrame:
        agg_ = []
        for aggregation in self.aggregations:
            func_=getattr(pyspark.sql.functions, aggregation.func)
            agg_+=([func_(col) for col in aggregation.cols])
        return df.groupBy(self.groupBy).agg(*agg_)


@dataclass_json
@dataclass
class ListLength(Transformation):
    """
    Calculates the length of a column of ArrayType.

    Args:
    ------
    col: String. Column with ArrayType.
    colName: String. Column name of column where to advise length of array in 'col'.

    ---- Example: ----
    ListLength(col='notes', colName='num_notes').transform(df).show()
    +------------+-----+---------+
    |       notes| name|num_notes|
    +------------+-----+---------+
    |[1, 2, 4, 2]|Alice|        4|
    |   [3, 4, 5]|  Bob|        3|
    +------------+-----+---------+

    """
    type = "ListLength"
    col: str = None
    colName: str = None

    def transform(self, df) -> DataFrame:
        return df.withColumn(
            colName=self.colName,
            col=F.size(self.col)
        )


@dataclass_json
@dataclass
class Month(Transformation):
    """
    Extract the month of a given date as integer.

    Args:
    ------
    date: String. Column with DateType where month to extract from.
    colName: String. Column name of month content.

    ---- Example: ----
    df = spark.createDataFrame([('2015-04-08',)], ['dt'])
    Month('dt', 'month').transform(df).collect()
    [Row(dt='2015-04-08', month=3)]
    """
    type = "Month"
    date: str = None
    colName: str = None

    def transform(self, df) -> DataFrame:
        return df.withColumn(colName=self.colName, col=(F.month(self.date)-1))


@dataclass_json
@dataclass
class Normalization(Transformation):
    type = "Normalization"
    col: str = None
    colName: str = None

    def transform(self, df):
        max=df.agg({"{}".format(self.col): "max"}).collect()[0][0]
        min = df.agg({"{}".format(self.col): "min"}).collect()[0][0]
        if max==min:
            return df.withColumn(self.colName, F.lit(0))
        return df.withColumn(self.colName, (df[self.col]- min) / (max - min))


@dataclass_json
@dataclass
class Percentage(Transformation):
    """
    Creates a column called 'percentage' with the percentage
    of the value in the column column.

    Args:
    ------
    col: String. Numerical Column which the percentage is calculated for
    colName: String.

    ---- Example: ----

    """
    type = "Percentage"
    col: str = None
    colName: str = None

    def transform(self, df):
        from pyspark.sql.window import Window
        import pyspark.sql.functions as f
        return df.withColumn(
            colName=self.colName,
            col=df[self.col] / f.sum(f.col(self.col)).over(Window.partitionBy())
        )


@dataclass_json
@dataclass
class Select(Transformation):
    """Projects a set of expressions and returns a new :class:`DataFrame`.

    Args:
    ------
    :param cols: list of column names (string) or expressions (:class:`Column`).
        If one of the column names is '*', that column is expanded to include all columns
        in the current :class:`DataFrame`.

    ---- Example: ----
    df.select('*').collect()
    [Row(age=2, name=u'Alice'), Row(age=5, name=u'Bob')]
    df.select('name', 'age').collect()
    [Row(name=u'Alice', age=2), Row(name=u'Bob', age=5)]
    df.select(df.name, (df.age + 10).alias('age')).collect()
    [Row(name=u'Alice', age=12), Row(name=u'Bob', age=15)]
    """
    type = "Select"
    cols: List[str] = None

    def transform(self, df):
        return df.select(self.cols)


@dataclass_json
@dataclass
class SortBy(Transformation):
    """Returns a new :class:`DataFrame` sorted by the specified column(s).

    Args:
    ------
    :param cols: list of :class:`Column` or column names to sort by.
    :param ascending: boolean or list of boolean (default ``True``).
        Sort ascending vs. descending. Specify list for multiple sort orders.
        If a list is specified, length of the list must equal length of the `cols`.

    ---- Example: ----
    SortBy("age", ascending=False).transform(df).collect()
    [Row(age=5, name=u'Bob'), Row(age=2, name=u'Alice')]
    df.orderBy(df.age.desc()).collect()
    [Row(age=5, name=u'Bob'), Row(age=2, name=u'Alice')]
    from pyspark.sql.functions import *
    df.sort(asc("age")).collect()
    [Row(age=2, name=u'Alice'), Row(age=5, name=u'Bob')]
    df.orderBy(desc("age"), "name").collect()
    [Row(age=5, name=u'Bob'), Row(age=2, name=u'Alice')]
    df.orderBy(["age", "name"], ascending=[0, 1]).collect()
    [Row(age=5, name=u'Bob'), Row(age=2, name=u'Alice')]
    """
    type = "SortBy"
    col: str = None
    ascending: bool = False

    def transform(self, df) -> DataFrame:
        return df.sort(self.col, ascending=self.ascending)


@dataclass_json
@dataclass
class Split(Transformation):
    """
    Splits str around pattern (pattern is a regular expression).

    .. note:: pattern is a string represent the regular expression.

    Args:
    ------
    col: String.
    colName: String.
    delimiter: String.


    ---- Example: ----
    df = spark.createDataFrame([('ab12cd',)], ['s',])
    df.select(split(df.s, '[0-9]+').alias('s')).collect()
    [Row(s=[u'ab', u'cd'])]
    """
    type = "Split"
    col: str = None
    colName: str = None
    delimiter: str = None

    def transform(self, df):
        return df.select(
            df['*'],
            F.split(F.col(self.col), self.delimiter).alias(self.colName)
        )


@dataclass_json
@dataclass
class Year(Transformation):
    """
    Extract the year of a given date as integer.

    Args:
    ------
    date: String. Column with DateType where year to extract from.
    colName: String. Column name of year content.

    ---- Example: ----
    df = spark.createDataFrame([('2015-04-08',)], ['dt'])
    Year('dt', 'year').transform(df).collect()
    [Row(dt='2015-04-08', year=2015)]
    """
    type = "Year"
    date: str = None
    colName: str = None

    def transform(self, df) -> DataFrame:
        return df.withColumn(colName=self.colName, col=F.year(self.date))
