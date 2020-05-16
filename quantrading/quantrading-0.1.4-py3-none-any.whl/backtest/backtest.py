import pandas as pd
from datetime import datetime, timedelta
from backtest.portfolio import Portfolio
from trading_day import TradingDay
from logger import bt_logger
import empyrical
import performance


# TradingDay.set_custom_trading_days(df.index.to_series().reset_index(drop=True))


class Algorithm:
    def __init__(self, **kwargs):
        self.name = None

        INITIAL_MONEY = kwargs.get("INITIAL_MONEY", None)
        if INITIAL_MONEY is None:
            self.portfolio = Portfolio()
        else:
            self.portfolio = Portfolio(INITIAL_MONEY=INITIAL_MONEY)

        self.start_date = None
        self.end_date = None
        self.date = None
        self.portfolio_log = pd.DataFrame()
        self.trading_days = TradingDay.all_trading_days.to_list()
        self.simulation_status = {}
        self.simulation_result = {}
        self.rebalancing_days = None
        self.market_df = None
        self.event_log = pd.DataFrame(columns=["datetime", "log"])

        self.exist_reservation_order = False
        self.reservation_order = pd.Series()

    def initialize(self):
        pass

    def on_data(self):
        pass

    def run(self):
        self.initialize()

        self.date = self.start_date
        end_date = self.end_date
        while self.date <= end_date:
            if self.is_trading_day():
                bt_logger.info(self.date)

                if self.exist_reservation_order:
                    self.execute_reservation_order()

                if self.is_rebalancing_day():
                    self.on_data()
                self.on_end_of_day()
            self.date += timedelta(days=1)
        self.on_end_of_algorithm()

    def execute_reservation_order(self):
        self.portfolio.set_allocations(self.reservation_order)
        self.reservation_order = pd.Series()
        self.exist_reservation_order = False

    def reserve_order(self, allocation: pd.Series):
        self.reservation_order = allocation
        self.exist_reservation_order = True

    def log_event(self, msg: str):
        self.event_log.loc[len(self.event_log)] = [self.date, msg]

    def is_trading_day(self):
        today = self.date
        if today in self.trading_days:
            return True
        else:
            return False

    def is_rebalancing_day(self):
        today = self.date
        if today in self.rebalancing_days:
            return True
        else:
            return False

    def on_start_of_day(self):
        pass

    def on_end_of_day(self):
        pass

    def on_end_of_algorithm(self):
        pass

    def log_portfolio_value(self):
        port_value = self.portfolio.get_total_portfolio_value()
        cash = self.portfolio.cash

        self.portfolio_log.loc[self.date, "port_value"] = port_value
        self.portfolio_log.loc[self.date, "cash"] = cash

        for ticker, amount in self.portfolio.security_holding.items():
            self.portfolio_log.loc[self.date, ticker + "_amount"] = amount

    def update_portfolio_value(self, market_df=None):
        if market_df is None:
            self.portfolio.update_holdings_value(self.date, self.market_df)
        else:
            self.portfolio.update_holdings_value(self.date, market_df)

    def set_holdings(self, ticker: str, weight: float):
        self.portfolio.set_weight(ticker, weight)

    def set_start_date(self, year: int, month: int, day: int):
        self.start_date = datetime(year, month, day)

    def set_end_date(self, year: int, month: int, day: int):
        date = datetime(year, month, day)
        assert date >= self.start_date
        self.end_date = date

    def set_rebalancing_days(self, date_list: list):
        self.rebalancing_days = [*date_list]

    def liquidate(self, ticker: str):
        self.set_holdings(ticker, 0)

    def get_daily_return(self):
        return self.portfolio_log['port_value'].pct_change()

    def get_result(self):
        portfolio_log = self.portfolio_log

        print(portfolio_log)
        result = self.get_result_from_portfolio_log(portfolio_log, self.rebalancing_days)

        return result

    @classmethod
    def get_result_from_portfolio_log(cls, portfolio_log, rebalancing_days):
        performance = calc_performance_from_value_history(portfolio_log["port_value"])

        portfolio_weight = portfolio_log.divide(portfolio_log['port_value'], axis=0)
        print(portfolio_log)
        print(portfolio_log['port_value'])
        # rebalancing_weight = portfolio_weight.loc[rebalancing_days]

        port_drawdown = performance.get("drawdown")
        portfolio_log = pd.concat([portfolio_log, port_drawdown], axis=1)
        performance["portfolio_log"] = portfolio_log

        result = dict()
        result['performance'] = performance
        # result['rebalancing_weight'] = rebalancing_weight
        return result

    @classmethod
    def simulation_result_to_excel_file(cls, file_name, result):
        performance = result['performance']
        rebalancing_weight = result['rebalancing_weight']

        portfolio_log = performance["portfolio_log"]
        monthly_returns = performance["monthly_returns"]
        annual_summary = performance["annual_summary"]
        performance_summary = performance["performance_summary"]
        with pd.ExcelWriter(f"./simulation_result/{file_name}.xlsx", datetime_format="yyyy-mm-dd") as writer:
            portfolio_log.to_excel(writer, sheet_name="portfolio log")
            rebalancing_weight.to_excel(writer, sheet_name="리밸런싱 비중")
            monthly_returns.to_excel(writer, sheet_name="월별수익률")
            annual_summary.to_excel(writer, sheet_name="연도별 요약")
            performance_summary.to_excel(writer, sheet_name="요약")

    @classmethod
    def simulation_result_to_excel_file2(cls, file_name, result):
        performance = result['performance']

        port_value = performance["port_value"]
        monthly_returns = performance["monthly_returns"]
        annual_summary = performance["annual_summary"]
        performance_summary = performance["performance_summary"]
        with pd.ExcelWriter(f"./simulation_result/{file_name}.xlsx", datetime_format="yyyy-mm-dd") as writer:
            port_value.to_excel(writer, sheet_name="포트밸류")
            monthly_returns.to_excel(writer, sheet_name="월별수익률")
            annual_summary.to_excel(writer, sheet_name="연도별 요약")
            performance_summary.to_excel(writer, sheet_name="요약")

    def result_to_excel(self, file_name=None, folder_name=None):
        if file_name is None:
            file_name = self.name

        if folder_name is None:
            path = f"./simulation_result/{file_name}.xlsx"
        else:
            path = f"./simulation_result/{folder_name}/{file_name}.xlsx"

        result = self.get_result()
        performance = result['performance']
        portfolio_log = performance["portfolio_log"]
        monthly_returns = performance["monthly_returns"]
        annual_summary = performance["annual_summary"]
        performance_summary = performance["performance_summary"]
        with pd.ExcelWriter(path, datetime_format="yyyy-mm-dd") as writer:
            portfolio_log.to_excel(writer, sheet_name="portfolio log")
            monthly_returns.to_excel(writer, sheet_name="월별수익률")
            annual_summary.to_excel(writer, sheet_name="연도별 요약")
            performance_summary.to_excel(writer, sheet_name="요약")
            self.event_log.to_excel(writer, sheet_name="event log")


def calc_performance_from_value_history(daily_values: pd.Series) -> dict:
    daily_returns = daily_values.pct_change()
    final_returns = daily_values.iloc[-1] / 100 - 1

    monthly_returns = empyrical.aggregate_returns(daily_returns, "monthly")
    yearly_returns = empyrical.aggregate_returns(daily_returns, "yearly")
    performance_summary = performance.get_performance_summary(daily_returns, final_returns)

    annual_std = performance.risk.get_annual_std(daily_returns)
    annual_summary = pd.concat([yearly_returns, annual_std], axis=1)
    annual_summary.columns = ["수익률", "변동성"]

    cumulative_returns = performance.returns.convert_values_to_cumulative_returns(daily_values)
    drawdown = performance.get_draw_down(cumulative_returns)

    return {
        "monthly_returns": monthly_returns,
        "yearly_returns": yearly_returns,
        "performance_summary": performance_summary,
        "annual_summary": annual_summary,
        "drawdown": drawdown
    }
