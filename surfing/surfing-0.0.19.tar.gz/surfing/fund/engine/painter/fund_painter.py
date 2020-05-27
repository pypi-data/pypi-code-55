import pandas as pd
import numpy as np
import platform
import matplotlib as mpl
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
from ....data.manager.score import FundScoreManager
CURRENT_PLATFORM = platform.system()
if CURRENT_PLATFORM == 'Darwin':
    mpl.rcParams['font.family'] = ['Heiti TC']
else:
    mpl.rcParams['font.family'] = ['STKaiti']

class FundPainter(object):

    @staticmethod
    def plot_fund_weights(  fund_weights_history:dict, 
                            fund_cash_history:dict, 
                            fund_marktet_price_history:dict):
        res = []
        for k,v in fund_weights_history.items():
            v = v
            v['date'] = k
            v['cash'] = fund_cash_history[k]  / fund_marktet_price_history[k]
            res.append(v)
        weights_df = pd.DataFrame(res).set_index('date')
        weights_df = weights_df.div(weights_df.sum(axis=1), axis=0)
        weights_df.fillna(0)[1:].plot.area(figsize=(18,9),legend=False,fontsize = 13)
        s = pl.title('fund weights history', fontsize=20)

    @staticmethod
    def plot_index_fund_fee( index_fee:pd.DataFrame):
        mpl.rcParams['font.size'] = 15
        p = index_fee.plot.pie(y='amount',figsize = (10,10))
        l = plt.legend(fontsize=13 ,loc = 'lower left')
        t = plt.title('index fee amount', fontsize=20)
        y = plt.ylabel(ylabel='fee amount', fontsize=14)

    @staticmethod
    def plot_fund_mdd_periods(  fund_mv:pd.DataFrame, 
                                fund_weights_history:dict, 
                                fund_nav:pd.DataFrame, 
                                fund_info:pd.DataFrame):
        df = fund_mv
        mdd_part1 = (df.loc[:, 'mv'] / df.loc[:, 'mv'].rolling(10000, min_periods=1).max())
        mdd_date1 = df.loc[:mdd_part1.idxmin(),'mv'].idxmax()
        mdd_date2 = mdd_part1.idxmin()
        date_list = np.array(list(fund_weights_history.keys()))
        date_list = date_list[(date_list >= mdd_date1) & (date_list <= mdd_date2)]
        fund_list = []
        for d in date_list:
            fund_list.extend([k for k,v in fund_weights_history[d].items() if isinstance(v, float) and (round(v,3) > 0)])
        fund_list = list(set(fund_list)) 
        if 'cash' in fund_list:
            fund_list.remove('cash')
        df = fund_nav[fund_list].loc[mdd_date1:mdd_date2,:] 
        if df.empty:
            return 
        fig, ax = plt.subplots(figsize= [18,9])
        df = df/df.iloc[0]
        table_df = fund_info.set_index('fund_id').loc[fund_list,:].reset_index()[['fund_id','desc_name','index_id']].sort_values(['index_id'])
        df_mdd = pd.DataFrame(((1-df.iloc[-1])*100).round(2))
        df_mdd.columns = ['max draw down %']
        table_df = table_df.set_index('fund_id').join(df_mdd).reset_index()
        fund_list = table_df.fund_id.tolist()
        
        for col in df.columns:
            plt.plot(df.index, df[[col]], linewidth=1.0, label = col)
        plt.legend(fontsize=13 ,loc = 'lower left')
        plt.title('fund bt during mdd period  nav of all funds', fontsize=20)
        ax.xaxis.set_ticks_position('top')
        t = plt.table(cellText=table_df.values.tolist(),
          colLabels=table_df.columns,
          colWidths= [0.25,0.45,0.15,0.15],  
          loc='bottom',
          )
        t.auto_set_font_size(False)
        t.auto_set_font_size(False)
        t.set_fontsize(15)
        t.auto_set_column_width('fund_id')
        t.AXESPAD = 0.1
        t.scale(1, 2)
        plt.show()

    @staticmethod
    def plot_fund_ret_each_year(turnover_df:pd.DataFrame,
                                mdd: float,
                                annual_ret: float):
        annual_ret = round(annual_ret, 3)
        mdd = round(mdd, 3)
        ret_year = round(turnover_df.year_ret.mean(), 3)
        p = turnover_df.set_index('year')[['year_mdd','year_ret']].plot.bar(figsize=(16,12))
        t = plt.title('return and mdd each year', fontsize=20)
        s = plt.suptitle(f'annual ret: {annual_ret}, ret mean {ret_year},mdd {mdd}', y=0.87, fontsize=15)
        h = plt.axhline(y=annual_ret, linestyle=':', label='annual ret', color='darkorange')
        r = plt.xticks(rotation=0)
        l = plt.legend(fontsize=13 ,loc='upper left')

    @staticmethod
    def plot_turnover_rate_each_year(turnover_df:pd.DataFrame, turnover_rate_yearly_avg:float):
        p = turnover_df.set_index('year')[['turnover_rate_yearly']].plot.bar(figsize=(16,12))
        t = plt.title('turnover rate each year %', fontsize=20)
        s = plt.suptitle(f'mean {turnover_rate_yearly_avg}', y=0.87, fontsize=15)
        y = turnover_df['turnover_rate_yearly'].mean()
        h = plt.axhline(y=y, linestyle=':', label='turnover rate mean')
        r = plt.xticks(rotation=0)
        l = plt.legend(fontsize=13 ,loc='upper left')

    @staticmethod
    def plot_fund_score(fund_mv:pd.DataFrame, 
                        fund_weights_history:dict, 
                        trade_history:dict,
                        index_price:pd.DataFrame,
                        asset_weights:dict,
                        fund_info:pd.DataFrame,
                        fund_nav:pd.DataFrame,
                        fund_score:dict,
                        fund_score_raw:dict,
                        fund_indicator:pd.DataFrame,
                        asset=str,
                        is_tuning=bool,
                        ):
        fund_w = fund_weights_history
        end_date = fund_mv.index.tolist()[-1]
        date_list = list(trade_history.keys()) + [end_date]
        fund_asset_df = fund_info[['fund_id','index_id']].set_index('fund_id')
        fund_indicator = fund_indicator.pivot_table(index = ['fund_id','datetime'])
        traded_to_submit_date = {}
        for d in trade_history:
            dic = trade_history[d][0]
            traded_to_submit_date[dic.trade_date] = dic.submit_date
        res = []
        for k,v in asset_weights.items():
            v['date'] = k
            res.append(v)
        weights_df = pd.DataFrame(res).set_index('date')
        weights_df = weights_df.drop(['cash'], axis = 1).dropna()[1:]
        res = []
        for dic, s in zip(weights_df.to_dict('records'), weights_df.sum(axis = 1).values):
            res.append({ k: v/ s for k, v in dic.items()})
        df = pd.DataFrame(res)
        cols = df.columns.tolist()
        name_dic = fund_info[['fund_id','desc_name']].set_index('fund_id')
        b_d = fund_nav.index[0]
        e_d = fund_nav.index[-1]
        bench_df = index_price.loc[b_d:e_d,[asset]]
        bench_df = bench_df/bench_df.iloc[0]
        for i in range(len(date_list) - 1):   
            b_d = date_list[i]
            e_d = date_list[i+1]
            if b_d == e_d:
                break
            bench_df_tmp = bench_df.loc[b_d:e_d,:]
            f_l = [k  for k ,v in fund_w[b_d].items() if isinstance(v, float) and round(v ,3 ) > 0]
            if 'cash' in f_l:
                f_l.remove('cash')
            f_l = [f for f in f_l if fund_asset_df.loc[f,'index_id'] == asset]
            mv_b = bench_df.loc[b_d,asset]
            fund_tmp = fund_nav.loc[b_d:e_d,f_l].copy()
            fund_tmp = fund_tmp/fund_tmp.iloc[0]
            fund_tmp = fund_tmp*mv_b
            res = []
            submit_d = traded_to_submit_date[b_d]
            if len(f_l) < 1:
                continue
            fig, ax = plt.subplots(figsize= [16,12])
            plt.plot(bench_df_tmp.index, bench_df_tmp[asset], label=asset,linewidth=5.0)
            for f in f_l:
                desc = name_dic.loc[f,'desc_name']
                f_i_dict= fund_indicator.loc[f,submit_d].to_dict()
                dic = {
                    'fund_id' : f,
                    'desc_name' : desc,
                    'score' : round(fund_score[submit_d][asset][f],4),
                    'weight': round(fund_w[b_d][f], 4),
                    'score_raw': round(fund_score_raw[submit_d][asset][f],4),
                }
                for s in ['alpha','beta','fee_rate','track_err']:
                    dic[s] = round(f_i_dict[s],4)
                res.append(dic)    
                plt.plot(fund_tmp.index, fund_tmp[f], label=f+'_'+desc,linestyle='--',linewidth=3.0)    
            
            if is_tuning:
                fund_not_select = [f for f, v in fund_score[submit_d][asset].items() if f not in f_l][:10]
                if len(fund_not_select) < 1:
                    break
                fund_tmp = fund_nav.loc[b_d:e_d,fund_not_select].copy()
                fund_tmp = fund_tmp/fund_tmp.iloc[0]
                fund_tmp = fund_tmp*mv_b
                for f in fund_not_select:
                    desc = name_dic.loc[f,'desc_name']
                    f_i_dict= fund_indicator.loc[f,submit_d].to_dict()
                    dic = {
                        'fund_id' : f,
                        'desc_name' : desc,
                        'score' : round(fund_score[submit_d][asset][f],4),
                        'weight': 0,
                        'score_raw': round(fund_score_raw[submit_d][asset][f],4),
                    }
                    for s in ['alpha','beta','fee_rate','track_err']:
                        dic[s] = round(f_i_dict[s],4)
                    res.append(dic)   
                    plt.plot(fund_tmp.index, fund_tmp[f], label=f+'_'+desc,linestyle=':',linewidth=3.0)    

            plt.legend(fontsize=15 ,loc = 'lower left')
            plt.title(f'{asset} {b_d} {e_d}', fontsize=25)
            plt.suptitle(FundScoreManager().funcs[asset].__dict__, y=0.87, fontsize=18)
            ax.xaxis.set_ticks_position('top')
            fund_df = pd.DataFrame(res)
            fund_df = fund_df[['desc_name','fund_id','weight','alpha','beta','track_err','fee_rate','score_raw','score']]
            fund_df = fund_df.sort_values('score', ascending = False)
            t = plt.table(
                cellText=fund_df.values.tolist(),
                colLabels=fund_df.columns,
                loc='bottom',
                colWidths= [0.25,0.12,0.09,0.09,0.09,0.09,0.09,0.09,0.09]          
            )
            t.auto_set_font_size(False)
            t.set_fontsize(15)
            t.auto_set_column_width('fund_id')
            t.AXESPAD = 0.1
            t.scale(1, 4)
            plt.show()