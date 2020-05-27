import time
import datetime
import pandas as pd
from pprint import pprint 
import operator
import traceback
from .backtest import FundBacktestEngine
from .trader import AssetTrader
from ...data.manager.manager_fund import FundDataManager
from ...data.struct import AssetTrade, FundTrade, FundScoreParam, TAAParam, TaaTunerParam, AssetTradeParam, AssetWeight
from ...data.api.derived import DerivedDataApi

class TaaTuner:

    BACKTEST_NUM = 3
    INDEX_WEIGHT = 0.1
    CASH_WEIGHT = 0.9
    TAA_LOW_TYPE = 'taa_low_only'
    TAA_UP_TYPE = 'taa_up_only'

    def __init__(self, start_time:str='20050101', end_time:str='20200501'):
        self.dm = FundDataManager(start_time=start_time, end_time=end_time)
        self.start_date = datetime.datetime.strptime(start_time, '%Y%m%d').date()
        self.end_date = datetime.datetime.strptime(end_time, '%Y%m%d').date()
        self.ap = AssetTradeParam()
        self.at = AssetTrader(self.ap)

    def init(self, taa_tuner:TaaTunerParam ):
        self.dm.init(score_pre_calc=False)
        self.taa_tuner = taa_tuner
        self.saa = AssetWeight(**{'cash':self.CASH_WEIGHT, self.taa_tuner.index_id:self.INDEX_WEIGHT})
        self.taa_type = self.TAA_LOW_TYPE if self.taa_tuner.IsTaaLowOnly else self.TAA_UP_TYPE
        self.bk_each_time = None

    def grid_search(self):
        self.run_saa()
        self.test_bk_time()
        self.search_bk()
        self.first_round_analysis()
        self.search_bk_2()
        self.second_round_analysis()

    def run_saa(self):
        saa_bk = FundBacktestEngine(data_manager=self.dm, trader=self.at, taa_params=None)
        saa_bk.init()
        saa_bk.run(saa=self.saa, start_date=self.start_date, end_date=self.end_date)
        self.saa_result = saa_bk._report_helper.get_asset_stat()
        
    def search_bk(self, is_test:bool=False, bk_list=None):
        if bk_list is None:
            if is_test:
                taa_param_list = self.taa_tuner.param_list[:self.BACKTEST_NUM]
            else:
                taa_param_list = self.taa_tuner.param_list
        else:
            taa_param_list = bk_list

        self.result = []
        c = 1
        bk_num = len(taa_param_list)
        if self.bk_each_time is not None:
            cost_min = len(taa_param_list) * self.bk_each_time / 60
            print(f'totally bk {bk_num} tasks index_id: {self.taa_tuner.index_id} may cost {cost_min} mins')
        else:
            print(f'totally bk {bk_num} tasks index_id: {self.taa_tuner.index_id}')
        for taa_i in taa_param_list:
            t_0 = time.time()
            taa_bk_i = FundBacktestEngine(data_manager=self.dm, trader=self.at, taa_params=taa_i)
            taa_bk_i.init()
            taa_bk_i.run(saa=self.saa, start_date=self.start_date, end_date=self.end_date)
            taa_result = taa_bk_i._report_helper.get_asset_stat()
            dic = taa_i.__dict__
            dic['taa_ret'] = taa_result['annual_ret']
            self.result.append(dic)
            t_1 = time.time()
            print(f'finish task {c}, cost {t_1 - t_0} sec')
            c += 1
        self.result = pd.DataFrame(self.result)
        self.result['saa_annual_ret'] = self.saa_result['annual_ret']
        self.result['taa_saa_annual_ret'] = self.result['taa_ret'] - self.saa_result['annual_ret']
        self.result['taa_type'] = self.taa_type
        self.result = self.result.sort_values('taa_saa_annual_ret', ascending=False)
        print()

    def test_bk_time(self):
        print()
        print('test backtest')
        t_0 = time.time()
        self.search_bk(is_test=True)
        t_1 = time.time()
        cost_time = t_1 - t_0
        self.bk_each_time = cost_time / self.BACKTEST_NUM
        print(f'bk {self.BACKTEST_NUM} times total cost {cost_time} sec, each bk {self.bk_each_time} sec')
        t_1 = time.time()
        task_num = len(self.taa_tuner.param_list)
        print(f'first round backtest may cost {task_num * self.bk_each_time / 60} mins')
        print()

    def first_round_analysis(self): 
        self.result.to_csv(f'{self.taa_tuner.index_id}_{self.taa_type}_round1.csv')
        self.first_round_result = self.result.iloc[0]
        print('first round filter result')
        pprint(self.first_round_result)
        print()

    def search_bk_2(self):
        d = self.first_round_result 
       
        self.bk_params = []
        if d.taa_type == self.TAA_UP_TYPE:
            LowThreshold = d.LowThreshold
            LowStop = d.LowStop
            LowPlus = d.LowPlus
            for HighMinus in [_ for _ in range( int(d.HighMinus * 100) - 1,int(d.HighMinus * 100) + 2, 1)]:
                for HighStop in [_ for _ in range( int(d.HighStop * 100) - 2,int(d.HighStop * 100) + 3, 1)]:
                    for HighThreshold  in [_ for _ in range( int(d.HighThreshold * 100) - 2,int(d.HighThreshold * 100) + 3, 1)]:
                        t = TAAParam()
                        t.HighThreshold = HighThreshold / 100
                        t.HighStop = HighStop / 100
                        t.HighMinus = HighMinus / 100
                        t.LowStop = LowStop 
                        t.LowThreshold = LowThreshold 
                        t.LowPlus = LowPlus 
                        t.TuneCash = True
                        self.bk_params.append(t)
        else:
            HighThreshold = d.HighThreshold
            HighStop = d.HighStop
            HighMinus = d.HighMinus
            for LowPlus in [_ for _ in range( int(d.LowPlus * 100) - 1,int(d.LowPlus * 100) + 2, 1)]:
                for LowStop in [_ for _ in range( int(d.LowStop * 100) - 2,int(d.LowStop * 100) + 3, 1)]:
                    for LowThreshold in [_ for _ in range( int(d.LowThreshold * 100) - 2,int(d.LowThreshold * 100) + 3, 1)]:
                        t = TAAParam()
                        t.HighThreshold = HighThreshold
                        t.HighStop = HighStop
                        t.HighMinus = HighMinus
                        t.LowStop = LowStop / 100
                        t.LowThreshold = LowThreshold / 100
                        t.LowPlus = LowPlus / 100
                        t.TuneCash = True
                        self.bk_params.append(t)
        self.search_bk(is_test=False, bk_list=self.bk_params)
        
    def second_round_analysis(self):
        self.result.to_csv(f'{self.taa_tuner.index_id}_{self.taa_type}_round2.csv')
        self.second_round_result = self.result.iloc[0]
        print('second round filter result')
        pprint(self.second_round_result)


class SaaTuner:

    ASSET_LIST = ['hs300', 'csi500', 'gem', 'sp500rmb', 'national_debt', 'gold']
    ROUND1_STEP = 5
    ROUND2_STEP = 1
    ROUND1_CSV = 'saa_tuner_round_1.csv'
    ROUND2_CSV = 'saa_tuner_round_2.csv'
    FINAL_CSV = 'saa_tuner_round_final.csv'

    def __init__(self, start_time:str='20050101', end_time:str='20200520'):
        self.dm = FundDataManager(start_time=start_time, end_time=end_time)
        self.start_date = datetime.datetime.strptime(start_time, '%Y%m%d').date()
        self.end_date = datetime.datetime.strptime(end_time, '%Y%m%d').date()
        self.derived = DerivedDataApi()

    def init(self):
        self.result_round1 = []
        self.result_round2 = []
        self.result_target = []
        self.dm.init(score_pre_calc=False)
        self.get_ports_saa()
        self.test_bk_time()
        
    def tune(self):
        self.first_round()
        self.second_round()
        self.final_round()

    def formal_print(self, sentence):
        print(sentence)
        print()

    def get_ports_saa(self):
        asset_info = self.derived.get_asset_allocation_info()
        asset_info = asset_info[['allocation_id','hs300','csi500','gem','sp500rmb','national_debt','gold','cash']].set_index('allocation_id')
        self.port_saa_dic = asset_info.to_dict('index')

    def bk_unit(self, asset:str, amt_diff:float):
        saa = AssetWeight(**{asset:10/100,'cash':90/100})
        asset_param = AssetTradeParam(EnableCommission=True, PurchaseDiscount=0.15, MinActionAmtDiff=amt_diff) 
        t = AssetTrader(asset_param)
        b = FundBacktestEngine(data_manager=self.dm, trader=t, taa_params=None)
        b.init()
        b.run(saa=saa,start_date=self.start_date, end_date=self.end_date)
        res = b.get_asset_result()
        return {'mdd': res['mdd'], 
                'annual_ret': res['annual_ret'], 
                'ret_over_mdd': res['ret_over_mdd'], 
                'asset': asset, 
                'amt_diff': amt_diff, 
                'start_date': self.start_date, 
                'end_date': self.end_date}

    def bk_unit_target(self, amt_diff:float):
        saa = AssetWeight(    
            hs300=15/100,
            csi500=5/100,
            gem=3/100,
            sp500rmb=7/100,
            national_debt=60/100,
            gold=7/100,
            cash=3/100
        )  
        asset_param = AssetTradeParam(EnableCommission=True, PurchaseDiscount=0.15, MinActionAmtDiff=amt_diff) 
        t = AssetTrader(asset_param)
        b = FundBacktestEngine(data_manager=self.dm, trader=t, taa_params=None)
        b.init()
        b.run(saa=saa,start_date=self.start_date, end_date=self.end_date)
        res = b.get_asset_result()
        return {'mdd': res['mdd'], 
                'annual_ret': res['annual_ret'], 
                'ret_over_mdd': res['ret_over_mdd'], 
                'amt_diff': amt_diff, 
                'start_date': self.start_date, 
                'end_date': self.end_date}
    
    def bk_input_saa_amt_diff(self, saa_dict:dict, amt_diff:float, port_id:int=0):
        try:
            saa = saa_dict#AssetWeight(saa_dict)  
            asset_param = AssetTradeParam(EnableCommission=True, PurchaseDiscount=0.15, MinActionAmtDiff=amt_diff) 
            t = AssetTrader(asset_param)
            b = FundBacktestEngine(data_manager=self.dm, trader=t, taa_params=None)
            b.init()
            b.run(saa=saa,start_date=self.start_date, end_date=self.end_date)
            res = b.get_asset_result()
            res['MinActionAmtDiff'] = amt_diff
            res['start_date'] = self.start_date
            res['end_date'] = self.end_date
            res['port_id'] = port_id
            return res
        except Exception as e:
            print(e)
            traceback.print_stack()
            print('boom')
            print(f'port_id {port_id} amt_diff {amt_diff}')
            print(saa_dict)    
            return None
        
    def test_bk_time(self):
        self.formal_print('test backtest')
        t_0 = time.time()
        asset = self.ASSET_LIST[0]
        amt_diff = [i/1000 for i in range(30,40,2)]
        for amt_diff_i in amt_diff:
            self.bk_unit(asset, amt_diff_i)
        t_1 = time.time()
        cost_time = t_1 - t_0
        self.bk_each_time = cost_time / len(amt_diff)
        self.formal_print(f'bk {len(amt_diff)} times total cost {cost_time} sec, each bk {self.bk_each_time} sec')
        
    def first_round(self):
        loop_layer_1 = self.ASSET_LIST
        loop_layer_2 = [_/10000 for _ in range(100, 905, self.ROUND1_STEP)]
        predict_time = len(loop_layer_1) * len(loop_layer_2) * self.bk_each_time / 60
        self.formal_print(f'###first round bk may cost {predict_time} mins')
        bk_time0 = time.time()
        for asset in loop_layer_1:
            asset_t0 = time.time()
            for amt_diff_i in loop_layer_2:
                self.result_round1.append(self.bk_unit(asset, amt_diff_i))
            asset_t1 = time.time()
            cost_m = (asset_t1 - asset_t0) / 60
            self.formal_print(f' - asset {asset} bk finish cost {cost_m} mins')
        bk_time1 = time.time()
        cost_m = (bk_time1 - bk_time0) / 60
        self.formal_print(f'first round finish cost cost {cost_m} mins')
        pd.DataFrame(self.result_round1).to_csv(self.ROUND1_CSV)

    def second_round(self):
        self.round1_df = pd.read_csv(self.ROUND1_CSV, index_col=0)
        loop_layer_1 = self.ASSET_LIST
        layer_2_lens = len([ i for i in range(-self.ROUND1_STEP+1, self.ROUND1_STEP, self.ROUND2_STEP)])
        predict_time = len(loop_layer_1) * layer_2_lens * self.bk_each_time / 60
        self.formal_print(f'###second round bk may cost {predict_time} mins')
        bk_time0 = time.time()
        for asset in loop_layer_1:
            amt_diff_0 = self.round1_df[self.round1_df.asset == asset].sort_values('ret_over_mdd', ascending=False).amt_diff.values[0]
            amt_diff_int = int(amt_diff_0 * 10000)
            for amt_diff_i in range(amt_diff_int - self.ROUND1_STEP + 1, amt_diff_int + self.ROUND1_STEP, self.ROUND2_STEP):
                amt_diff_i = amt_diff_i / 10000
                self.result_round2.append(self.bk_unit(asset, amt_diff_i))
        bk_time1 = time.time()
        cost_m = (bk_time1 - bk_time0) / 60
        self.formal_print(f'second round finish cost cost {cost_m} mins')
        pd.DataFrame(self.result_round2).to_csv(self.ROUND2_CSV)

    def final_round(self):
        self.round2_df = pd.read_csv(self.ROUND2_CSV, index_col=0)
        res = []
        for asset in self.ASSET_LIST:
            res_i = self.round2_df[self.round2_df.asset == asset].sort_values('ret_over_mdd', ascending=False).reset_index(drop=True).iloc[0]
            res.append(res_i)
        self.final_df = pd.DataFrame(res)
        self.formal_print('###final result sort by ret over mdd')
        print(self.final_df)
        self.final_df.to_csv(self.FINAL_CSV)
    
    def target_backtest(self):
        loop_layer = [_/10000 for _ in range(100, 905, self.ROUND1_STEP)]
        for amt_diff_i in loop_layer:
            self.result_target.append(self.bk_unit_target(amt_diff_i))
        self.target_df = pd.DataFrame(self.result_target)
        res = self.target_df.sort_values('ret_over_mdd', ascending=False).reset_index(drop=True).head()
        print(res)

    def bk_fee_search(self, fee_con:bool, MinActionAmtDiff:float):
        saa = AssetWeight(    
            hs300=15/100,
            csi500=5/100,
            gem=3/100,
            sp500rmb=7/100,
            national_debt=60/100,
            gold=7/100,
            cash=3/100
        )  
        asset_param = AssetTradeParam(EnableCommission=fee_con, PurchaseDiscount=0.15, MinActionAmtDiff=MinActionAmtDiff) 
        t = AssetTrader(asset_param)
        b = FundBacktestEngine(data_manager=self.dm, trader=t, taa_params=None)
        b.init()
        b.run(saa=saa,start_date=self.start_date, end_date=self.end_date)
        res = b.get_asset_result()
        res['MinActionAmtDiff'] = MinActionAmtDiff
        res['fee_status'] = fee_con
        res['start_date'] = self.start_date
        res['end_date'] = self.end_date
        return res

    def search_fee(self):
        self.result_fee = []
        #for fee_con in [True, False]:
        fee_con = False
        for MinActionAmtDiff in [0.02,0.03,0.04,0.05,0.06,0.065,0.07,0.08]:
            res_i = self.bk_fee_search(fee_con, MinActionAmtDiff)
            self.result_fee.append(res_i)
        #self.result_fee_df = pd.DataFrame(self.result_fee)

    def bk_unit_double_asset(self, saa, amt_dif):
        asset_param = AssetTradeParam(EnableCommission=True, PurchaseDiscount=0.15, MinActionAmtDiff=amt_dif) 
        t = AssetTrader(asset_param)
        b = FundBacktestEngine(data_manager=self.dm, trader=t, taa_params=None)
        b.init()
        b.run(saa=saa)
        res = b.get_asset_result()
        res['amt_dif'] = amt_dif
        res['rebalance_details'] = b._trader.rebalance_details
        return res

    def bk_loop_selected_amt_diff(self, asset_1, asset_2):
        result = []
        for w in range(10,91,2):
            saa = AssetWeight(**{asset_1:w/100,asset_2:(99-w)/100, 'cash':1/100})
            amt_dif = 50 / 1000
            res_i = self.bk_unit_double_asset(saa=saa, amt_dif=amt_dif)
            result.append(res_i)
        return pd.DataFrame(result)

    def find_trigger_asset(self, dic):
        res = []
        for d, k in dic.items():
            if k:
                res.append({'date':d,'trigger_asset':max(k.items(), key=operator.itemgetter(1))[0]})
        trigger_list = pd.DataFrame(res).trigger_asset.tolist()
        trigger_dic = {i: trigger_list.count(i) for i in set(trigger_list)}
        trigger_asset = max(trigger_dic.items(), key=operator.itemgetter(1))[0]
        return trigger_asset

    def find_trigger_process(self, asset_1, asset_2):
        result = self.bk_loop_selected_amt_diff(asset_1,asset_2)
        res = []
        for idx, r in result.iterrows():
            if len(r.rebalance_date) == 2:
                res.append('unvalid bk, rebalence time <= 2')
                continue
            if idx == 0:
                res.append('None')
                continue
            trigger_asset=self.find_trigger_asset(r.rebalance_details)
            res.append(trigger_asset)
        result['trigger_asset'] = res
        result['rebalance_times'] = [len(_) for _ in result['rebalance_date']]
        return result

if __name__ == "__main__":
    
    tt = TaaTunerParam()
    tt.IsTaaUpOnly = True
    tt.index_id = 'hs300'

    LowStop = -100
    LowThreshold = -100
    LowPlus = 0

    tt.param_list = []
    for HighThreshold in range(80, 97, 2):
        for HighStop in range(50, 71, 2):
            for HighMinus in [3 , 5, 7]:
                t = TAAParam()
                t.HighThreshold = HighThreshold / 100
                t.HighStop = HighStop / 100
                t.HighMinus = HighMinus / 100
                t.LowStop = LowStop / 100
                t.LowThreshold = LowThreshold / 100
                t.LowPlus = LowPlus / 100
                t.TuneCash = True
                tt.param_list.append(t)

    bk = TaaTuner()
    bk.init(tt)   
    bk.grid_search()

    '''
    asset_1 = 'hs300'
    asset_2 = 'csi500'
    hs300_csi500 = find_trigger_process(asset_1, asset_2)
    hs300_csi500[[asset_1,asset_2,'trigger_asset','rebalance_times']]
    '''