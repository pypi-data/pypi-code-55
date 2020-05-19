from pyspark.sql.dataframe import DataFrame
from pyspark_config.spark_utils.functions import DataFrame_Functions
from pyspark_config.spark_utils.table_from_database import Table
from typing import List


class DataFrame_Extended(DataFrame):
    """
    this class extends the DataFrame class by all functions
    defined in the class DataFrame_Functions as staticmethods.

    Attributes:
    -----------
    df: pyspark.sql.DataFrame
        dataFrame which is desired to extend
    spark_session: pyspark.sql.SparkSession
        sparkSession which is used during the execution

    Methods:
    -----------
    get_table_from_database: DataFrame_Extended class
        enables the user to obtain the dataFrame from a database
    add_date: DataFrame_Extended class
        creates 'year', 'month', 'day' to the given dataFrame
    add_weekday: DataFrame_Extended class
        creates 'weekday' to the given dataFrame

    """
    def __init__(self, df, spark_session):
        super(self.__class__, self).__init__(df._jdf, df.sql_ctx)
        self.df: DataFrame=df
        self.spark_session = spark_session

    @classmethod
    def get_table_from_database(cls, spark_session, df_name):
        df_ = Table(spark_session=spark_session, table_name=df_name).table
        return cls(df=df_, spark_session=spark_session)

    def select(self, cols: List[str]):
        df = DataFrame_Functions.select(df=self.df, cols=cols)
        return DataFrame_Extended(df=df, spark_session=self.spark_session)

    def filter(self, sql_condition):
        """Filters rows using the given condition.

        :func:`where` is an alias for :func:`filter`.

        :param condition: a :class:`Column` of :class:`types.BooleanType`
            or a string of SQL expression.

        df.filter(df.age > 3).collect()
        [Row(age=5, name=u'Bob')]
        df.where(df.age == 2).collect()
        [Row(age=2, name=u'Alice')]

        df.filter("age > 3").collect()
        [Row(age=5, name=u'Bob')]
        df.where("age = 2").collect()
        [Row(age=2, name=u'Alice')]
        """
        df = DataFrame_Functions.filter(df=self.df, sql_condition=sql_condition)
        return DataFrame_Extended(df=df, spark_session=self.spark_session)

    def filter_by_list(self, col: str, choice_list:List[str]):
        df = DataFrame_Functions.filter_by_list(
            df=self.df, col=col,
            choice_list=choice_list
        )
        return DataFrame_Extended(df=df, spark_session=self.spark_session)

    def cast(self,col: str,newCol: str,fromType: str,toType: str):
        df = DataFrame_Functions.cast(
            df=self.df,
            col=col,
            newCol=newCol,
            fromType=fromType,
            toType=toType
        )
        return DataFrame_Extended(df=df, spark_session=self.spark_session)

    def sort(self, column, ascending=False):
        """
        Returns a new :class:`DataFrame_Extended` sorted by the specified column(s).

        :param cols: list of :class:`Column` or column names to sort by.
        :param ascending: boolean or list of boolean (default True).
            Sort ascending vs. descending. Specify list for multiple sort orders.
            If a list is specified, length of the list must equal length of the `cols`.
        """
        df = DataFrame_Functions.sort(df=self.df, column=column, ascending=ascending)
        return DataFrame_Extended(df=df, spark_session=self.spark_session)

    def normalization(self, col, newCol):
        df = DataFrame_Functions.normalization(df=self.df, col=col, newCol=newCol)
        return DataFrame_Extended(df=df, spark_session=self.spark_session)

    def groupby(self, groupBy_col_list, sum_col_list: List[str]=None,
                count_col_list: List[str]=None):
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
        df = DataFrame_Functions.groupby(
            df=self.df,
            groupBy_col_list=groupBy_col_list,
            sum_col_list=sum_col_list,
            count_col_list=count_col_list
        )
        return DataFrame_Extended(df=df, spark_session=self.spark_session)

    def join_customized(self, other, left_on: List[str], right_on: List[str], how: str):
        df=DataFrame_Functions.join(
            left=self.df,
            right=other,
            left_on=left_on,
            right_on=right_on,
            how=how
        )
        return DataFrame_Extended(df=df, spark_session=self.spark_session)

    def concatenate(self, cols, name, delimiter=""):
        """
        Creates a column with the indicated columns concatenated with the delimiter (Default: "").

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
        df = DataFrame_Functions.concatenate(
            df=self.df,
            cols=cols,
            name=name,
            delimiter=delimiter
        )
        return DataFrame_Extended(df=df, spark_session=self.spark_session)

    def split(self, column, newCol, delimiter):
        df = DataFrame_Functions.split(
            df=self.df,
            column=column,
            newCol=newCol,
            delimiter=delimiter
        )
        return DataFrame_Extended(df=df, spark_session=self.spark_session)

    def applyFastText(self,delimiter,originalCol,column,newCol,size,window,min_count,epoche):
        df = DataFrame_Functions.applyFastText(
            df=self.df,
            spark_session=self.spark_session,
            delimiter=delimiter,
            originalCol=originalCol,
            column=column,
            newCol=newCol,
            size=size,
            window=window,
            min_count=min_count,
            epoche=epoche
        )
        return DataFrame_Extended(df=df, spark_session=self.spark_session)

    def add_date(self, date):
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
        date: String
            Column with DateType

        :return: DataFrame_Extended

        """
        df=DataFrame_Functions.add_date(df=self.df, date=date)
        return DataFrame_Extended(df=df, spark_session=self.spark_session)

    def add_weekday(self, date):
        """
        Creates a numerical column 'weekday' with the
        corresponding weekday with
            1 for monday,
            2 for tuesday,
            3 for wednesday,
            4 for thursday,
            5 for friday,
            6 for saturday,
            7 for sunday

        Attributes:
        -----------
        date: String
            Column with DateType

        :return: DataFrame_Extended

        """
        df=DataFrame_Functions.add_weekday(df=self.df, date=date)
        return DataFrame_Extended(df=df, spark_session=self.spark_session)

    def add_perc(self, column, perc_name):
        """
        Creates a column called 'percentage' with the percentage
        of the value in the column column.

        Attributes:
        -----------
        column: String
            Numerical Column which the percentage is calculated for

        :return: DataFrame_Functions

        """
        df = DataFrame_Functions.add_perc(
            df=self.df,
            column=column,
            perc_name=perc_name,
            spark_session=self.spark_session
        )
        return DataFrame_Extended(
            df=df,
            spark_session=self.spark_session
        )

    def collect_list(self, order_by, group_by_list, column_list):
        df = DataFrame_Functions.collect_list(
            df=self.df,
            order_by=order_by,
            group_by_list=group_by_list,
            column_list=column_list
        )
        return DataFrame_Extended(
            df=df,
            spark_session=self.spark_session
        )

    def list_length(self, column):
        df = DataFrame_Functions.list_length(
            df=self.df,
            column=column
        )
        return DataFrame_Extended(
            df=df,
            spark_session=self.spark_session
        )

    def one_hot_encoder(self, col, newCol, vocabSize):
        df = DataFrame_Functions.one_hot_encoder(
            df=self.df,
            col=col,
            newCol=newCol,
            vocabSize=vocabSize
        )
        return DataFrame_Extended(
            df=df,
            spark_session=self.spark_session
        )

    def cluster_df(self, cluster_col, cluster_list,
                   groupby_col_list: list=[], sum_col_list: list=[],
                   count_col_list: list=[]):
        df = DataFrame_Functions.cluster_df(
            df=self.df,
            cluster_col=cluster_col,
            cluster_list=cluster_list,
            groupby_col_list=groupby_col_list,
            sum_col_list=sum_col_list,
            count_col_list=count_col_list
        )
        return DataFrame_Extended(
            df=df,
            spark_session=self.spark_session
        )