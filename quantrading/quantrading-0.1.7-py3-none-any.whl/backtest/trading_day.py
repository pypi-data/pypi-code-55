from datetime import datetime
import pandas as pd
import calendar

DEFAULT_DATE_FORMAT = "%Y-%m-%d"


class TradingDay:
    def __init__(self, trading_days: list):
        self.all_trading_days = pd.Series(trading_days).sort_values().reset_index(drop=True)
        self.first_date = self.all_trading_days.iloc[0]
        self.last_date = self.all_trading_days.iloc[-1]

    def get_trading_day_list(self, start_date: datetime, end_date: datetime) -> pd.Series:
        trading_days = self.all_trading_days
        trading_days = trading_days[trading_days >= start_date]
        trading_days = trading_days[trading_days <= end_date]
        return trading_days

    def get_rebalancing_days(self,
                             start_date: datetime,
                             end_date: datetime,
                             rebalancing_periodic: str,
                             rebalancing_moment: str) -> pd.Series:
        if rebalancing_periodic == 'daily':
            rebalancing_days = self.get_trading_day_list(start_date, end_date)
        elif rebalancing_periodic == 'monthly':
            start_month = start_date.strftime("%Y-%m")
            end_month = end_date.strftime("%Y-%m")
            if rebalancing_moment == 'first':
                rebalancing_days = self.get_first_day_of_every_month(start_month, end_month)
            elif rebalancing_moment == 'last':
                rebalancing_days = self.get_last_day_of_every_month(start_month, end_month)
            else:
                raise ValueError("Invalid rebalancing_moment type : ", rebalancing_moment)
        elif rebalancing_periodic == 'quarterly':
            start_quarter = f"{start_date.year}-{(start_date.month - 1) // 3 + 1}"
            end_quarter = f"{end_date.year}-{(end_date.month - 1) // 3 + 1}"
            rebalancing_days = self.get_first_day_of_report_month(start_quarter, end_quarter)
        else:
            raise ValueError("Invalid rebalancing_periodic type : ", rebalancing_periodic)
        return rebalancing_days

    def get_first_day_of_every_month(self, start_date: str, end_date: str):
        """
        ex) 2002Y,2M -> "2002-2"
        ex) 2015Y,12M -> "2015-12"
        """
        year_n_month_combination = generate_year_n_month(start_date, end_date)
        days = []
        for year, month in year_n_month_combination:
            first_date = f"{year}-{month}-1"
            temp_date = self.magnet(first_date, 1)
            days.append(temp_date)
        return days

    def get_last_day_of_every_month(self, start_date: str, end_date: str):
        """
        example
        date: 2019-12
        """
        year_n_month_combination = generate_year_n_month(start_date, end_date)
        days = []
        for year, month in year_n_month_combination:
            temp_trading_days = self.get_trading_days_by_year_n_month(year, month)
            last_date = temp_trading_days.tolist()[-1]
            days.append(last_date)
        return days

    def magnet(self, date, flag):
        """
        flag: before:0, after:1
        """
        if flag == 1:
            trading_days = self.get_trading_day_list(date, self.last_date)
            near_date = trading_days.iloc[0]
        elif flag == 0:
            trading_days = self.get_trading_day_list(self.first_date, date)
            near_date = trading_days.iloc[-1]
        else:
            raise ValueError(f"Invalid flag : {flag}")
        return near_date

    def get_trading_days_by_year_n_month(self, year, month):
        end_month_last_day = calendar.monthrange(year, month)[1]
        start_date = f"{year}-{month}-01"
        end_date = f"{year}-{month}-{end_month_last_day}"
        start_date = datetime.strptime(start_date, DEFAULT_DATE_FORMAT)
        end_date = datetime.strptime(end_date, DEFAULT_DATE_FORMAT)

        trading_date_series = self.get_trading_day_list(start_date, end_date)
        return trading_date_series

    def get_first_day_of_report_month(self, start_date: str, end_date: str):
        year_n_month_combination = generate_year_n_month(start_date, end_date)
        days = []
        for year, month in year_n_month_combination:
            if month not in [4, 6, 9, 12]:
                continue
            first_date = f"{year}-{month}-1"
            temp_date = self.magnet(first_date, 1)
            days.append(temp_date)
        return days

    # @classmethod
    # def set_custom_trading_days(cls, trading_days):
    #     cls.all_trading_days = trading_days
    #     first_date = trading_days.iloc[0]
    #     last_date = trading_days.iloc[-1]
    #     cls.LOWER_BOUND_DATE = first_date
    #     cls.UPPER_BOUND_DATE = last_date

    # @classmethod
    # def get_trading_days_between_date(cls, start_date, end_date):
    #     """
    #     example
    #     T+0, T+2 => 2일
    #     T+10, T+50 => 40일
    #     """
    #     tradings_days = cls.get_trading_day_list(start_date, end_date)
    #     return len(tradings_days) - 1
    #
    # @classmethod
    # def get_trading_days_by_year(cls, year):
    #     start_date = f"{year}-01-01"
    #     end_date = f"{year}-12-31"
    #     trading_date_series = cls.get_trading_day_list(start_date, end_date)
    #     return trading_date_series
    #
    # @classmethod
    # def get_trading_days_by_year_n_month(cls, year, month):
    #     end_month_last_day = calendar.monthrange(year, month)[1]
    #     start_date = f"{year}-{month}-01"
    #     end_date = f"{year}-{month}-{end_month_last_day}"
    #
    #     trading_date_series = cls.get_trading_day_list(start_date, end_date)
    #     return trading_date_series
    #
    #
    # @classmethod
    # def get_date_of_every_year(cls, start_year: int, end_year: int, month: int, day: int, before_if_close=True):
    #     """
    #     after_if_close: 0:before, 1:after
    #     """
    #     if before_if_close:
    #         flag = 0
    #     else:
    #         flag = 1
    #
    #     days = []
    #     for year in range(start_year, end_year + 1):
    #         n_th_date = f"{year}-{month}-{day}"
    #         temp_date = cls.magnet(n_th_date, flag)
    #         days.append(temp_date)
    #     return days
    #
    # @classmethod
    # def get_first_day_of_every_week(cls, start_date: str, end_date: str):
    #     every_monday_list = generate_every_monday(start_date, end_date)
    #     days = []
    #     for date in every_monday_list:
    #         temp_date = cls.magnet(date, 1)
    #         days.append(temp_date)
    #     return days
    #
    #
    #
    # @classmethod
    # def get_n_th_day_of_every_month(cls, start_date: str, end_date: str, n_th: int, before_if_close=True):
    #     """
    #     example
    #     date: 2019-12
    #
    #     after_if_close: 0:before, 1:after
    #     """
    #     if before_if_close:
    #         flag = 0
    #     else:
    #         flag = 1
    #
    #     year_n_month_combination = generate_year_n_month(start_date, end_date)
    #     days = []
    #     for year, month in year_n_month_combination:
    #         n_th_date = f"{year}-{month}-{n_th}"
    #         temp_date = cls.magnet(n_th_date, flag)
    #         days.append(temp_date)
    #     return days
    #
    # @classmethod
    # def get_14th_day_of_every_month(cls, start_date: str, end_date: str):
    #     """
    #     example
    #     date: 2019-12
    #     """
    #     year_n_month_combination = generate_year_n_month(start_date, end_date)
    #     days = []
    #     for year, month in year_n_month_combination:
    #         _14th_date = f"{year}-{month}-14"
    #         temp_date = cls.magnet(_14th_date, 0)
    #         days.append(temp_date)
    #     return days
    #
    # @classmethod
    # def get_15th_day_of_every_month(cls, start_date: str, end_date: str):
    #     """
    #     example
    #     date: 2019-12
    #     """
    #     year_n_month_combination = generate_year_n_month(start_date, end_date)
    #     days = []
    #     for year, month in year_n_month_combination:
    #         _15th_date = f"{year}-{month}-15"
    #         temp_date = cls.magnet(_15th_date, 0)
    #         days.append(temp_date)
    #     return days
    #
    # @classmethod
    # def get_last_day_of_every_quarter(cls, start_quarter: str, end_quarter: str):
    #     """
    #     example
    #     YYYY-Q
    #     Q(Quarter) : 1 ~ 4
    #     date: 2019-1
    #     :return:
    #     """
    #     year_n_quarter_combination = generate_year_n_quarter(start_quarter, end_quarter)
    #     days = []
    #     for year, quarter in year_n_quarter_combination:
    #         month = quarter * 3
    #         temp_trading_days = cls.get_trading_days_by_year_n_month(year, month)
    #         last_date = temp_trading_days.tolist()[-1]
    #         days.append(last_date)
    #     return days


def generate_year_n_month(start_date: str, end_date: str):
    start_year, start_month = start_date.split("-")
    end_year, end_month = end_date.split("-")
    start_year = int(start_year)
    start_month = int(start_month)
    end_year = int(end_year)
    end_month = int(end_month)

    combinations = []
    # start year
    combinations += [(start_year, month) for month in range(start_month, 13)]

    # middle years
    if start_year < (end_year - 1):
        combinations += [(year, month) for year in range(start_year + 1, end_year) for month in range(1, 13)]

    # end year
    if start_year != end_year:
        combinations += [(end_year, month) for month in range(1, end_month + 1)]

    return combinations


def generate_year_n_quarter(start_quarter: str, end_quarter: str):
    start_year, start_quarter = start_quarter.split("-")
    end_year, end_quarter = end_quarter.split("-")
    start_year = int(start_year)
    start_quarter = int(start_quarter)
    end_year = int(end_year)
    end_quarter = int(end_quarter)

    combinations = []
    # start year
    combinations += [(start_year, quarter) for quarter in range(start_quarter, 5)]

    # middle years
    if start_year < (end_year - 1):
        combinations += [(year, quarter) for year in range(start_year + 1, end_year) for quarter in range(1, 5)]

    # end year
    if start_year != end_year:
        combinations += [(end_year, quarter) for quarter in range(1, end_quarter + 1)]

    return combinations


def generate_every_monday(start_date: str, end_date: str):
    every_monday_list = pd.date_range(start_date, end_date, freq="W-MON")
    return every_monday_list
