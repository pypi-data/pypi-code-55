import numpy as np
import pandas as pd
import random as math_random
from sklearn.preprocessing import minmax_scale


class Transform:
    """
    Applies on df, returns always a new copy of a df fitting that condition
    """

    @staticmethod
    def calculate_daily_change(df):
        change = df.copy()
        for fips in change.columns:
            tmp = 0
            for date in change.index:
                v = change.at[date, fips]
                change.at[date, fips] = max(0, v - tmp)
                tmp = v
        return change

    # @staticmethod
    # def find_first_column_with_a_value_greater(df, x):

    @staticmethod
    def partition(v, i):
        """

        :param v:
        :param i:
        :return:
        """
        if i > 0:
            return v[0:i], v[i + 1:]
        else:
            n = len(v)
            return v[0:n + i], v[i:]

    @staticmethod
    def shuffle(v):
        math_random.shuffle(v)
        return v

    @staticmethod
    def partition_by_percent(v, first, second):
        """

        :param v:
        :param first:
        :param second:
        :return:
        """
        if first + second != 100:
            raise ValueError("partition_y_percent: The two values must add up to 100")
        n = round(len(v) * first / 100)
        return Transform.partition(v, n)

    @staticmethod
    def remove_between(df, start_date, end_date):
        r = df.loc[(df.index >= start_date) & (df.index <= end_date)]
        return r

    @staticmethod
    def get_time_period(df, start_date="1999-01-01", end_date="2050-01-01", inplace=False):
        if inplace:
            select = df
        else:
            select = df.copy()
        t0 = pd.to_datetime(start_date)
        t1 = pd.to_datetime(end_date)
        select = select.loc[(select.index >= start_date) & (select.index <= end_date)]
        return t0, t1, select

    @staticmethod
    def find_first_columns_with_value_greater(df, x):
        """
        finds first date that is greater than x and eliminates all dates before that time

        :param df:
        :param x:
        :return:
        """
        a = df.copy().transpose()
        for day in df.index:
            v = a[day].to_list()
            count = len([i for i in v if i > x])
            if count > 0:
                break
            elif count == 0:
                a = a.drop(columns=[day])
        a = a.transpose()
        return a

    @staticmethod
    def find_from_first_non_zero(df):
        """
        finds first date that is non zero and eliminates all data before that date

        :param df: dataframe
        :return: new df
        """
        """
        """
        a = df.copy().transpose()
        for day in df.index:
            s = a[day].sum()

            if s > 0:
                break
            elif s == 0:
                a = a.drop(columns=[day])
        a = a.transpose()
        return a

    @staticmethod
    def remove_if_smaller(df, x):
        """
        removes all rows if they only contain values smaller than x
        careful, this could eliminate others in future too

        see also: find_first_columns_with_value_greater(df, x)

        :param df:
        :param x:
        :return:
        """
        data = df.copy().transpose()
        data = data[data.columns[(data > x).any()]]
        data = data.transpose()
        return data

    @staticmethod
    def remove_if_greater(df, x):
        """
        removes all rows if they only contain values smaller than x
        careful, this could eliminate others in future too

        see also: find_first_columns_with_value_greater(df, x)

        :param df:
        :param x:
        :return:
        """
        data = df.copy().transpose()
        data = data[data.columns[(data < x).any()]]
        data = data.transpose()
        return data


class Normalize:  # normalize dataframe

    @staticmethod
    def remove_negative_values(df, value=0):
        df[df < 0] = value
        return df

    @staticmethod
    def minmaxscalar(df):
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        df[df.columns] = scaler.fit_transform(df[df.columns])
        return df

    @staticmethod
    def log_normalize(v):
        result = np.log(v + 1)
        result = minmax_scale(result, feature_range=(0, 1))
        return result

    @staticmethod
    def zero_to_one(df):
        df = Normalize.matrix(df)
        return df

    @staticmethod
    def matrix(df):
        result = df.copy()
        min_value = df.min().min()
        max_value = df.max().max()
        result = (result - min_value) / (max_value - min_value)
        return result

    @staticmethod
    def log(df, attribute):
        return np.log((df.loc[:, attribute] + 1).tolist())

    @staticmethod
    def columns(df, which=None, f=None):  # f = np.log
        """
        Takes a column, finds its maximum and normalizes it to have
        min = 0 and max = 1
        """
        if f == "log":
            f = Normalize.log
        result = df.copy()
        if which is None:
            which = result.which
        for column in which:
            max_value = df[column].max()
            min_value = df[column].min()
            result[column] = (df[column] - min_value) / (max_value - min_value)
            if f is not None:
                print(type(result[column]))
                result[column] = f(result, column)
        return result

    @staticmethod
    def rows(df, which=None, f=None):
        """
        Takes a column, finds its maximum and normalizes it to have
        min = 0 and max = 1
        """
        result = df.copy().transpose()
        result = Normalize.columns(result, which=which, f=f)
        result = result.transpose()
        return result
