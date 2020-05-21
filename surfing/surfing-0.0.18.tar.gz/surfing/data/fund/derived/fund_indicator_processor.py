
import pandas as pd
import numpy as np
import datetime
from pyfinance.ols import PandasRollingOLS
import traceback
from ...manager.manager_fund import FundDataManager
from ...manager.score import FundScoreManager
from ...struct import AssetWeight
from ...wrapper.mysql import DerivedDatabaseConnector
from ...view.derived_models import FundIndicator

class FundIndicatorProcessor(object):

    TRADING_DAYS_PER_YEAR = 242
    SHORT_TIME_SPAN = TRADING_DAYS_PER_YEAR
    LONG_TIME_SPAN = TRADING_DAYS_PER_YEAR * 3
    LONG_TERM_INDEX = ['hs300', 'csi500', 'mmf']

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

    def get_beta(self, fund_ret, index_ret, time_range):
        # beta 贝塔 
        # 表示基金的收益相对与基准对变化， 绝对值越大， 相对于基准波动越大， 体现为风险越大
        # rf: 基金日收益  rm: 基准日收益 
        # rf = beta * rm + C （滚动计算）
        res = []
        index_id = index_ret.columns[0]
        for fund_id in fund_ret.columns:
            df = fund_ret[[fund_id]].join(index_ret)
            x = df[index_id]
            y = df[fund_id]
            model = PandasRollingOLS(y=y, x=x, window=time_range)
            res_i = model.beta
            res_i.columns = [fund_id]
            res.append(res_i)
        return res

    def get_alpha(self,fund_ret, index_ret, time_range):
        # alpha 阿尔法
        # 表示超越市场的收益
        # rf_avg 基金平均收益 rb_avg 基准平均收益
        # alpha = (rf_avg - beta * rb_avg) * year
        fund_list = fund_ret.columns.tolist()
        index_id = index_ret.columns[0]
        rf_avg = fund_ret.rolling(time_range).mean().reindex(self.beta.index)
        rb_avg = index_ret.rolling(time_range).mean().reindex(self.beta.index)
        v1 = self.beta[fund_list].multiply(rb_avg.values, axis=index_id).copy()
        alpha_i = (rf_avg - v1) * self.TRADING_DAYS_PER_YEAR
        return alpha_i
    
    def get_track_error(self,fund_ret, index_ret, time_range):
        # track error 跟踪误差
        # 表示跟踪基准的能力
        # track_error = (rf-rb).std
        fund_list = fund_ret.columns.tolist()
        index_id = index_ret.columns[0]
        res = []
        for fund_id in fund_list:
            df = fund_ret[[fund_id]].join(index_ret)
            track_err_i = (df[fund_id] - df[index_id]).rolling(time_range).std( ddof=1 ) #按照天天基金的算法， 不年化
            res.append(track_err_i)
        df = pd.DataFrame(res).T
        df.columns = fund_list
        return df

    def upload_derived(self, df, table_name):
        print(table_name)
        df.to_sql(table_name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')

        if table_name not in self.updated_count:
            self.updated_count[table_name] = 0
        self.updated_count[table_name] += df.shape[0]

    def calculate(self):
        res = []
        for index_id in self.index_list:
            time_range = self.get_time_range(index_id)
            fund_list = self.index_fund[index_id]
            fund_ret = self.fund_ret.loc[index_id][fund_list].copy()
            index_ret = self.index_ret[[index_id]]
            res.extend(self.get_beta(fund_ret, index_ret, time_range))
        self.beta = pd.concat(res, axis=1, sort=True) 
        
        res_alpha = []
        res_track_err = []
        for index_id in self.index_list:
            time_range = self.get_time_range(index_id)
            fund_list = self.index_fund[index_id]
            fund_ret = self.fund_ret.loc[index_id][fund_list].copy()
            index_ret = self.index_ret[[index_id]]
            res_alpha.append(self.get_alpha(fund_ret, index_ret, time_range))
            res_track_err.append(self.get_track_error(fund_ret, index_ret, time_range))
        
        self.alpha = pd.concat(res_alpha, axis=1, sort=True)  
        self.track_err = pd.concat(res_track_err, axis=1, sort=True)  

        fac_list = ['beta','alpha','track_err']
        data_list = [self.beta, self.alpha, self.track_err]
        res = []
        for name, data in zip(fac_list, data_list):
            df = data.stack().reset_index(level=[0,1]).copy()
            df = df.rename(columns = {'level_0':'datetime','level_1':'fund_id',0:'value'})
            df['name'] = name
            res.append(df.copy())
        self.result = pd.concat(res).pivot_table(index=['datetime','fund_id'], columns='name',values='value')

        self.fund_fee = self.fund_info[['fund_id','manage_fee','trustee_fee']].set_index('fund_id').fillna(0).sum(axis = 1)
        self.fund_fee = pd.DataFrame(self.fund_fee).rename(columns = {0:'fee_rate'})
        span_dic = {}
        for index_id, fund_list in self.index_fund.items():
            time_span = int(self.get_time_range(index_id) / self.TRADING_DAYS_PER_YEAR)
            for fund_id in fund_list:
                span_dic[fund_id] = time_span
        self.fund_fee['timespan'] = self.fund_fee.index.map(lambda x : span_dic.get(x,0)).tolist()
        self.result = self.result.join(self.fund_fee).reset_index(level=[0,1])

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
