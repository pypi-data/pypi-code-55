
import pandas as pd
import numpy as np
import datetime
import traceback
from ...manager.manager_fund import FundDataManager
from ...manager.score import FundScoreManager
from ...wrapper.mysql import DerivedDatabaseConnector
from ...view.derived_models import FundIndicator

class FundIndicatorProcessor(object):

    TRADING_DAYS_PER_YEAR = 242
    SHORT_TIME_SPAN = TRADING_DAYS_PER_YEAR
    LONG_TIME_SPAN = TRADING_DAYS_PER_YEAR * 3
    LONG_TERM_INDEX = ['hs300', 'csi500', 'mmf']
    MIN_TIME_SPAN = int(TRADING_DAYS_PER_YEAR / 4)#为了延长基金回测范围，评分最低年限3个月

    def __init__(self):
        self.updated_count = {}

    def init(self, start_date, end_date):    
        self._dm = FundDataManager(start_time=start_date, end_time=end_date, score_manager=FundScoreManager())
        self._dm.init(score_pre_calc=False)
        self.start_date = self._dm.start_date
        self.end_date = self._dm.end_date
        self.fund_nav = self._dm.dts.fund_nav.copy()
        self.fund_info = self._dm.dts.fund_info.copy()
        self.index_price = self._dm.dts.index_price.copy()
        
        # 指数日线价格和基金净值 时间轴对齐 ，避免join后因为日期不存在出现价格空值
        # 指数数据历史上出现非交易日有数据，join后，基金净值出现空值，长周期时间序列算指标出空值 
        # 避免对日收益fillna(0)， 造成track error 计算不符合实际
        # 计算逻辑空值填充情况： 1. 只对基金费率空值fillna(0) 
        #                    2. manager fund 里对日线价格ffill
        #                    3. 指数数据按照基金数据重做index后ffill(有基金数据对日子,没有指数数据，比如季报出在季度末，非交易日有基金净值)
        #                    4. 有对超过基金终止日净值赋空值
        end_date = min(self.fund_nav.index[-1], self.index_price.index[-1])
        self.fund_nav = self.fund_nav.loc[:end_date]
        self.index_price = self.index_price[:end_date]
        fund_nav_index = self.fund_nav.index
        self.index_price = self.index_price.reindex(fund_nav_index).fillna(method = 'ffill')
        l1 = self.fund_nav.index.to_list().sort()
        l2 = self.index_price.index.to_list().sort()
        assert l1 == l2, f'date index of index price and fund nav are not identical, l1 {l1} lens {len(l1)}, l2 {l2} lens {len(l2)}'

        fund_to_enddate_dict = self.fund_info[['fund_id', 'end_date']].set_index('fund_id').to_dict()['end_date']
        self.fund_to_index_dict = self.fund_info[['fund_id', 'index_id']].set_index('fund_id').to_dict()['index_id']
        # 超过基金终止日的基金净值赋空
        for fund_id in self.fund_nav.columns:
            fund_end_date = fund_to_enddate_dict[fund_id]
            if self.end_date > fund_end_date:
                self.fund_nav.loc[fund_end_date:,fund_id] = np.nan

        self.index_ret = np.log(self.index_price / self.index_price.shift(1))
        self.fund_ret = np.log(self.fund_nav / self.fund_nav.shift(1))
        self.fund_ret = self.fund_ret.stack().reset_index(level=[0,1]).rename(columns={0:'ret'})        
        self.fund_ret['index_id'] = self.fund_ret.fund_id.apply(lambda x: self.fund_to_index_dict[x])
        self.fund_ret = self.fund_ret.pivot_table(index = ['index_id','datetime'],columns='fund_id',values='ret')
        self.index_ret = np.log(self.index_price / self.index_price.shift(1))
        self.fund_to_index_dict = {fund_id:index_id for fund_id,index_id in self.fund_to_index_dict.items() if fund_id in self.fund_ret.columns}
        self.index_list = self.fund_ret.index.levels[0]
        self.index_fund = { index_id : [fund_idx for fund_idx, index_idx in self.fund_to_index_dict.items() if index_idx == index_id] for index_id in self.index_list}
        
    def get_time_range(self, index_id):
        if index_id in self.LONG_TERM_INDEX:
            return self.LONG_TIME_SPAN
        else:
            return self.SHORT_TIME_SPAN

    ''' 
    尝试过几个版本的回归函数， 计算结果一致
    1. 最早使用的是pyfinance.PandasRollingOLS  可以对一只基金直接返回beta, alpha, 可以设置滚动周期, 运算比较快， 缺点是无法设置min_periods，最小滚动周期
    2. pyfinance.PandasRollingOLS 本质是使用statsmodels.regression.rolling.RollingOLS, 需要手动增加回归常数项，函数下存在最小窗口设置，但是使用无效，
       而且window实际的含义和pandas.rolling.window有区别，导致计算有效值和nan的边界时间不一致
    3. np.polyfit 一元回归，自带回归常数项，可以设置回归最高幂

    为了实现增加最小窗口设置功能的滑动回归， 用pandas.rolling对df.index做滑动计算（验证过不能用datetime index， 只能用整数序列），通过index选取多个列，进行回测
    TODO pandas.rolling 只能返回一列，尝试过一些方法，未果，实质上beta和alpha是同一次回归一起返回的，当前只能分两次计算，增加运算时间
    '''

    def _roll_beta(self, x):
        b_d = int(x[0])
        e_d = int(x[-1])
        df_i = self.df.loc[b_d:e_d,].copy()
        if sum(df_i.fund) == 0:
            return np.Inf
        else:
            res = np.polyfit(y=df_i.fund, x=df_i.benchmark,deg=1)
            return res[0]

    def _roll_alpha(self, x):
        b_d = int(x[0])
        e_d = int(x[-1])
        df_i = self.df.loc[b_d:e_d,].copy()
        if sum(df_i.fund) == 0:
            return np.Inf
        else:
            res = np.polyfit(y=df_i.fund, x=df_i.benchmark,deg=1)
            return res[1] * self.TRADING_DAYS_PER_YEAR

    def upload_derived(self, df, table_name):
        print(table_name)
        df.to_sql(table_name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')
        if table_name not in self.updated_count:
            self.updated_count[table_name] = 0
        self.updated_count[table_name] += df.shape[0]

    def calculate(self, index_id_list:str=None):
        self.fund_fee = self.fund_info[['fund_id','manage_fee','trustee_fee']].set_index('fund_id').fillna(0).sum(axis = 1)
        res = []
        index_list = self.index_list if index_id_list is None else index_id_list
        for index_id in index_list:
            time_range = self.get_time_range(index_id)
            fund_list = self.index_fund[index_id]
            fund_ret = self.fund_ret.loc[index_id][fund_list].copy()
            index_ret = self.index_ret[[index_id]]
            for fund_id in fund_list:
                self.df = fund_ret[[fund_id]].join(index_ret).dropna()
                self.df = self.df.rename(columns={index_id:'benchmark',fund_id:'fund'}).reset_index()
                self.df['beta'] = pd.Series(self.df.index).rolling(window=time_range,min_periods=self.MIN_TIME_SPAN).apply(self._roll_beta,raw=True)
                self.df['alpha'] = pd.Series(self.df.index).rolling(window=time_range,min_periods=self.MIN_TIME_SPAN).apply(self._roll_alpha,raw=True)
                self.df['track_err'] = (self.df.fund - self.df.benchmark).rolling(window=time_range, min_periods=self.MIN_TIME_SPAN).std(ddof=1) 
                self.df['fund_id'] = fund_id
                self.df['timespan'] = int(time_range / self.TRADING_DAYS_PER_YEAR)
                self.df['fee_rate'] = self.fund_fee[fund_id]
                self.df = self.df.drop(['fund','benchmark'], axis=1)
                res.append(self.df)
            print(f'index {index_id} fund number : {len(fund_list)} finish' )
        self.result = pd.concat(res, axis=0).replace(np.Inf,None).dropna()

    def process(self, start_date, end_date):
        failed_tasks = []
        try:
            start_date_dt = datetime.datetime.strptime(start_date, '%Y%m%d').date()
            end_date_dt = datetime.datetime.strptime(end_date, '%Y%m%d').date()

            start_date = start_date_dt - datetime.timedelta(days = 1150) #3年历史保险起见，多取几天 3*365=1095 
            start_date = datetime.datetime.strftime(start_date, '%Y%m%d')

            self.init(start_date, end_date)
            self.calculate()
            df = self.result[(self.result['datetime'] >= start_date_dt) & (self.result['datetime'] <= end_date_dt)]

            self.upload_derived(df, FundIndicator.__table__.name)
        except Exception as e:
            print(e)
            traceback.print_stack()
            failed_tasks.append('fund_indicator')

        return failed_tasks
