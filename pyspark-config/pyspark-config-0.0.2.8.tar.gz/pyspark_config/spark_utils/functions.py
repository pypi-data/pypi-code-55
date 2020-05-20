import pyspark.sql.functions as F
import datetime
from pyspark.sql.functions import udf, year, month, dayofmonth, date_format, dayofyear
from pyspark.sql import DataFrame, Window
from pyspark.sql.types import ArrayType, StringType, IntegerType
from typing import List
from pyspark.ml.feature import CountVectorizer


class DataFrame_Functions(object):
    """
    functions in order to extend the dataFrame class

    Methods:
    -----------
    filter: pyspark.sql.DataFrame
        Filters rows using the given condition.
    sort: pyspark.sql.DataFrame
        Returns a new :class:`DataFrame` sorted by
        the specified column(s).
    add_date: pyspark.sql.DataFrame
        creates 'year', 'month', 'day' to the given dataFrame
    add_weekday: pyspark.sql.DataFrame
        creates 'weekday' to the given dataFrame
    calculate_percentage: pyspark.sql.DataFrame
        creates a column called 'percentage' with the percentage
        of the value in the column column.
    """

    @staticmethod
    def select(
            df: DataFrame,
            cols: List[str]
    ) -> DataFrame:
        return df.select(cols)

    @staticmethod
    def filter(
            df,
            sql_condition
    )  -> DataFrame:
        """
        Filters rows using the given condition.

        :func:`where` is an alias for :func:`filter`.

        :param condition: a :class:`Column` of :class:`sources.BooleanType`
            or a string of SQL expression.
        """
        return df.filter(sql_condition)

    @staticmethod
    def filter_by_list(
            df,
            col: str,
            choice_list:List[str]
    ) -> DataFrame:
        return df.where((F.col(col).isin(choice_list)))

    @staticmethod
    def cast(
        df,
        col: str,
        newCol: str,
        fromType: str,
        toType: str
    ) -> DataFrame:
        casted_column=df[col].cast(toType)
        return df.withColumn(newCol, casted_column)

    @staticmethod
    def conditional(
            df, cond: str,
            value=None,
            col_target: str=None,
            fillna=None
    ):
        if value==None and col_target==None:
            raise TypeError("Both parameters 'value' and 'col_target' are ")
        target=value if value else col_target
        new_col=df.sql('WHEN {} THEN  {} ELSE {}').format(cond, )

    @staticmethod
    def normalization(df, col, newCol):
        max=df.agg({"{}".format(col): "max"}).collect()[0][0]
        min = df.agg({"{}".format(col): "min"}).collect()[0][0]
        if max==min:
            return df.withColumn(newCol, F.lit(0))
        return df.withColumn(newCol, (df[col]- min) / (max - min))

    @staticmethod
    def max(df, cols: List[str]):
        return df.select(F.greatest(cols))

    @staticmethod
    def min(df, cols: List[str]):
        return df.select(F.least(cols))

    @staticmethod
    def sort(df, column, ascending=False):
        """
        Returns a new :class:`DataFrame` sorted by the specified column(s).

        :param cols: list of :class:`Column` or column names to sort by.
        :param ascending: boolean or list of boolean (default True).
            Sort ascending vs. descending. Specify list for multiple sort orders.
            If a list is specified, length of the list must equal length of the `cols`.
        """
        return df.sort(column, ascending=ascending)

    @staticmethod
    def groupby(df, groupBy_col_list, sum_col_list:list=[],
                count_col_list:list=[]):
        """"Groups the :class:`DataFrame` using the specified columns,
        so we can run aggregation on them. See :class:`GroupedData`
        for all the available aggregate functions.

        :func:`groupby` is an alias for :func:`groupBy`.

        :param groupBy_col_list: list of columns to group by.
            Each element should be a column name (string) or an expression (:class:`Column`).
        :param sum_col_list: list of columns to sum by groups.
            Each element should be a column name (string) or an expression (:class:`Column`).
        :param count_col_list: list of columns to count by groups.
            Each element should be a column name (string) or an expression (:class:`Column`).

        """
        sum_list=[F.sum(col).alias('{}_sum'.format(col)) for col in sum_col_list]
        count_list=[F.count(col).alias('{}_count'.format(col)) for col in count_col_list]
        agg_list=sum_list+count_list

        return df.groupBy(
            groupBy_col_list
        ).agg(
            *agg_list
        )

    @staticmethod
    def join(left, right, left_on: List[str], right_on: List[str], how:str):
        """Joins with another :class:`DataFrame`, using the given join expression.

        :param other: Right side of the join
        :param on: a string for the join column name, a list of column names,
            a join expression (Column), or a list of Columns. If `on` is a string or a
            list of strings indicating the name of the join column(s), the column(s)
            must exist on both sides, and this performs an equi-join.
        :param how: str, default ``inner``. Must be one of: ``inner``, ``cross``,
            ``outer``,``full``, ``full_outer``, ``left``, ``left_outer``, ``right``,
            ``right_outer``, ``left_semi``, and ``left_anti``.

        """
        def get_on(left_on, right_on):
            if len(left_on) != len(right_on):
                raise IndexError("list 'left_on' and list 'right_on' "
                                 "must have the same length.")
            elif len(left_on)==0 and len(right_on)==0:
                raise IndexError("list 'left_on' and list 'right_on' "
                                 "must have at least one entry.")
            else:
                return [F.col(f) == F.col(s) for (f, s) in zip(left_on, right_on)]
        return left.join(
            other=right,
            on=get_on(left_on, right_on),
            how=how
        )

    @staticmethod
    def concatenate(df, cols, name, delimiter=""):
        """
        Creates a column with the indicated columns concatenated with a delimiter (Default: "").

        :param df: DataFrame

        :param cols: List[String]
            Columns to concatenate. Column type must be a string
        :param name: String
            Column name of the concatenated column
        :param delimiter: String
            Specifies the boundary between separate columns in the concatenated sequence

        :return: DataFrame
            DataFrame with created concatenation column

        """
        concat_udf = F.udf(lambda cols: delimiter.join([x if x is not None else "" for x in cols]), StringType())
        return df.select(
            df['*'],
            concat_udf(F.array(*cols)).alias(name)
        )

    @staticmethod
    def split(df, column, newCol, delimiter=""):
        return df.select(
            df['*'],
            F.split(F.col(column), delimiter).alias(newCol)
        )

    @staticmethod
    def add_date(
            df: DataFrame,
            date: str
    ) -> DataFrame:
        """
        Creates three columns 'year', 'month', 'day' with
            1  for january,
            2  for february,
            3  for march,
            4  for april,
            5  for may,
            6  for june,
            7  for july,
            8  for august,
            9  for september,
            10 for october,
            11 for november,
            12 for december

        Attributes:
        -----------
        df: pyspark.sql.DataFrame
            DataFrame of interest
        date: String
            Column with DateType

        :return: pyspark.sql.DataFrame

        """
        return df.select(
            df["*"],
            year(date).alias('year'),
            (month(date)-1).alias('month'),
            (dayofmonth(date)-1).alias('day'),
            (dayofyear(date)-1).alias('dayofyear')
        )

    @staticmethod
    def add_weekday(
            df: DataFrame,
            date: str
    ) -> DataFrame:
        """
        Creates a numerical column 'weekday' with the corresponding weekday with
            1 for monday,
            2 for tuesday,
            3 for wednesday,
            4 for thursday,
            5 for friday,
            6 for saturday,
            7 for sunday

        Attributes:
        -----------
        df: pyspark.sql.DataFrame
            DataFrame of interest
        date: String
            Column with DateType

        :return: pyspark.sql.DataFrame

        """
        return df.select(
            df["*"],
            date_format(date, 'u').alias('weekday')
        )

    @staticmethod
    def add_perc(
            df: DataFrame,
            column: str,
            spark_session,
            perc_name="perc"
    ) -> DataFrame:
        """
        Creates a column called percentage_name with default name 'perc'
        with the percentage of the value in the column column.

        Attributes:
        -----------
        df: pyspark.sql.DataFrame
            DataFrame of interest
        column: String
            Numerical Column which the percentage is calculated for
        perc_name: String
            Column name of the new column, by default 'perc'
        spark_session: pyspark.sql.SparkSession
            Current spark session for execution

        :return: pyspark.sql.DataFrame

        """
        from pyspark.sql.window import Window
        import pyspark.sql.functions as f
        return df.withColumn(perc_name, df[column]/f.sum(f.col(column)).over(Window.partitionBy()))

    @staticmethod
    def collect_list(
            df,
            order_by,
            group_by_list,
            column_list
    ) -> DataFrame:
        """
        Aggregate function: returns a list of objects with duplicates.

        :param df:
        :param group_by_list:
        :param column:
        :return:
        """

        w = Window.partitionBy(group_by_list).orderBy(order_by)

        def column_wise(df, column):
            new_column_name='{}_list'.format(column)
            return  df.withColumn(
                new_column_name,
                F.collect_list(df[column]).over(w)
            )

        def column_wise_(column):
            new_column_name='{}_list'.format(column)
            return  F.max(new_column_name).alias(new_column_name)

        column_list_=[column_wise_(column) for column in column_list]
        for column in column_list:
            df=column_wise(df, column)
        return df.groupby(group_by_list).agg(*column_list_)

    @staticmethod
    def list_length(df, column):
        return df.select(
            df["*"],
            F.size(column).alias('{}_cnt'.format(column))
        )

    @staticmethod
    def one_hot_encoder(df, col, newCol, vocabSize):
        return CountVectorizer(
            inputCol=col,
            outputCol=newCol,
            vocabSize=vocabSize,
            minDF=1.0
        ).fit(df).transform(df)

    @staticmethod
    def min_by_group(df, colName, column, groupByList):
        w = Window.partitionBy(groupByList)
        df.withColumn(
            colName,
            df.over(w).min(column)
        )


    @staticmethod
    def add_difference_time_series(df, column):
        """
        returns a list of objects with duplicates

        Attributes:
        ------------
        df: pyspark.sql.DataFrame
            DataFrame of interest
        column: String
            Column with type List() which the percentage is calculated for

        """
        def stringToDate(date_time_str):
            return datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
        def get_days(t1, t2):
            delta=stringToDate(t2) - stringToDate(t1)
            return delta.days
        def difference_dates(dateList):
            return [get_days(t1, t2) for t1, t2 in zip(dateList[:-1], dateList[1:])]
        udf_difference_dates= udf(lambda dateList: difference_dates(dateList), ArrayType(IntegerType()))
        return df.select(
            df["*"],
            udf_difference_dates(df[column]).alias("date_dif_time_serie")
        )

    @staticmethod
    def cluster_df(df,cluster_col, cluster_list,
                   groupby_col_list: list=[], sum_col_list: list=[],
                   count_col_list: list=[]):
        """

        """
        def aux_func(x, cluster_list):
            return  x if x in cluster_list else 'OTHERS'

        udf_clustering = udf(lambda dateList: aux_func(dateList, cluster_list))

        df=df.select(
            df['*'],
            udf_clustering(df[cluster_col]).alias('cluster_aux')
        )

        sum_list = [F.sum(col).alias('{}_sum'.format(col)) for col in sum_col_list]
        count_list = [F.count(col).alias('{}_count'.format(col)) for col in count_col_list]
        agg_list = sum_list + count_list
        return df.groupBy(
            groupby_col_list+['cluster_aux']
        ).agg(
            *agg_list
        )
