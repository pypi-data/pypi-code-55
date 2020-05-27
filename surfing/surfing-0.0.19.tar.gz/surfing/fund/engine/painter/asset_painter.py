import pandas as pd
import platform
import matplotlib as mpl
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
from ....data.struct import TAAParam
CURRENT_PLATFORM = platform.system()
if CURRENT_PLATFORM == 'Darwin':
    mpl.rcParams['font.family'] = ['Heiti TC']
else:
    mpl.rcParams['font.family'] = ['STKaiti']

class AssetPainter(object):

    @staticmethod
    def plot_asset_weights(asset_weight_dic:dict):
        asset_weight_df = pd.DataFrame(asset_weight_dic).T
        res = []
        for dic, s in zip(asset_weight_df.to_dict('records'), asset_weight_df.sum(axis = 1).values):
            res.append({ k: v/ s for k, v in dic.items()})
        df = pd.DataFrame(res)
        cols = df.columns.tolist()
        cols = [col for col in cols if df[col].sum() != 0]
        df = df[cols]
        df.index = asset_weight_df.index
        df.plot.area(figsize=(18,9),legend=False,fontsize = 13)
        l = pl.legend(loc='lower left',fontsize = 9)
        s = pl.title('asset weights history', fontsize=20)

    @staticmethod
    def plot_asset_mdd_period(asset_mv:pd.DataFrame, saa_weight:dict, index_price: pd.DataFrame):
        df = asset_mv
        mdd_part1 = (df.loc[:, 'mv'] / df.loc[:, 'mv'].rolling(10000, min_periods=1).max())
        mdd_date1 = df.loc[:mdd_part1.idxmin(),'mv'].idxmax()
        mdd_date2 = mdd_part1.idxmin()
        l = [k for k, v in saa_weight.items() if v > 0]
        l.remove('cash')
        df = index_price.copy()[l].loc[mdd_date1:mdd_date2].fillna(method='bfill')
        if df.empty:
            return 
        df = df / df.iloc[0]
        df.plot.line(figsize=(18,9),legend=False,fontsize = 13)
        l = pl.legend(loc='lower left',fontsize = 13)
        s = pl.title('asset bt during mdd period  price of holding assets', fontsize=20)    

    @staticmethod
    def plot_asset_taa_saa(saa_mv:pd.DataFrame, taa_mv:pd.DataFrame, index_id:str, index_pct:pd.DataFrame):
        taa_mv = taa_mv.rename(columns = {'mv':'taa'})
        saa_mv = saa_mv.rename(columns = {'mv':'saa'})
        begin_d = index_pct[[index_id]].index.values[0]
        df1 = saa_mv[['saa']].join(taa_mv['taa'])
        df1 = (df1 / df1.iloc[0])
        df1.plot.line(figsize=(20,12),legend=False,fontsize = 13)
        l = pl.legend(loc='upper left',fontsize = 25)
        s = pl.title(f'{index_id} taa', fontsize=20)

    @staticmethod
    def plot_taa_analysis(saa_mv:pd.DataFrame, taa_mv:pd.DataFrame, index_id:str, index_pct:pd.DataFrame, taa_params:TAAParam, index_price:pd.DataFrame):
        def _plot_pct_high(ax, high_i, df, price_col):
            start = mdates.date2num(high_i['start_date'])
            end = mdates.date2num(high_i['end_date'])
            width = end - start
            price_max = df.loc[high_i['start_date']: high_i['end_date']][price_col].max() 
            bottom = high_i['end_pct'] 
            height = price_max - bottom
            rect = Rectangle((start, bottom), width, height, color='greenyellow')
            ax.add_patch(rect)   

        def _plot_pct_low(ax, low_i, df, price_col):
            start = mdates.date2num(low_i['start_date'])
            end = mdates.date2num(low_i['end_date'])
            width = end - start
            price_max = df.loc[low_i['start_date']: low_i['end_date']][price_col].max() 
            bottom = low_i['start_pct'] 
            height = price_max - bottom
            rect = Rectangle((start, bottom), width, height, color='cornsilk')
            ax.add_patch(rect)   

        def _plot_dif(ax, low_i, df, is_add):
            start = mdates.date2num(low_i['start_date'])
            end = mdates.date2num(low_i['end_date'])
            width = end - start
            price_max = df.loc[low_i['start_date']: low_i['end_date']]['taa/saa'].max() 
            bottom = df.loc[low_i['start_date']: low_i['end_date']]['taa/saa'].min() 
            height = price_max - bottom
            if is_add:
                c = 'cornsilk'
            else:
                c = 'greenyellow'
            rect = Rectangle((start, bottom), width, height, color=c)
            ax.add_patch(rect)   

        
        high_threshold = taa_params.HighThreshold
        low_threshold = taa_params.LowThreshold
        high_stop = taa_params.HighStop
        low_stop = taa_params.LowStop
        high_minus = taa_params.HighMinus
        low_plus = taa_params.LowPlus

        pct_col = index_id + '_pct'
        price_col = index_id + '_price'
        pct_df = index_pct[[index_id]].rename(columns= {index_id:f'{index_id}_pct'})
        price_df = index_price[['hs300','csi500','gem','sp500rmb']].rename(columns= {   
                                                                            'hs300':'hs300_price',
                                                                            'csi500':'csi500_price',
                                                                            'gem':'gem_price',
                                                                            'sp500rmb':'sp500rmb_price'
                                                                            })
        df = pct_df[[pct_col]].join(price_df[[price_col]]).dropna()
        df[price_col] = df[price_col] / df[price_col][0]

        # taa high part
        taa_con = False
        high_minus_periods = []
        for d, r in df.iterrows():
            if taa_con == False and r[pct_col] >= high_threshold:
                taa_con = True
                dic = {'start_date': d}
                dic['start_price'] = r[price_col]
                dic['start_pct'] = r[pct_col]
            elif taa_con == True and r[pct_col] <= high_stop:
                dic['end_date'] = d
                dic['end_price'] = r[price_col]
                dic['end_pct'] = r[pct_col]
                dic['high_avoid_pct'] = dic['end_price'] / dic['start_price'] - 1
                high_minus_periods.append(dic)
                taa_con = False
            if d == df.index[-1] and taa_con == True:
                dic['end_date'] = d
                dic['end_price'] = r[price_col]
                dic['end_pct'] = r[pct_col]
                dic['high_avoid_pct'] = dic['end_price'] / dic['start_price'] - 1
                high_minus_periods.append(dic)

        # taa low part
        taa_con = False
        low_plus_periods = []
        for d, r in df.iterrows():
            if taa_con == False and r[pct_col] <= low_threshold:
                taa_con = True
                dic = {'start_date': d}
                dic['start_price'] = r[price_col]
                dic['start_pct'] = r[pct_col]
            elif taa_con == True and r[pct_col] >= low_stop:
                dic['end_date'] = d
                dic['end_price'] = r[price_col]
                dic['end_pct'] = r[pct_col]
                dic['low_gain_pct'] = dic['end_price'] / dic['start_price'] - 1
                low_plus_periods.append(dic)
                taa_con = False
            if d == df.index[-1] and taa_con == True:
                dic['end_date'] = d
                dic['end_price'] = r[price_col]
                dic['end_pct'] = r[pct_col]
                dic['low_gain_pct'] = dic['end_price'] / dic['start_price'] - 1
                low_plus_periods.append(dic)

        fig, ax = plt.subplots(figsize= [20,12])
        plt.plot(df.index, df[pct_col], label = pct_col, linewidth=2.0)
        plt.plot(df.index, df[price_col], label = price_col, linewidth=2.0)
        plt.legend(fontsize=20 ,loc = 'upper left')
        plt.title(f'{index_id} TAA ', fontsize=30)
        plt.suptitle(f'high_threshold {high_threshold}  low_threshold {low_threshold}  high_stop {high_stop} low_stop {low_stop}',  
                    y=0.87, fontsize=18)
        for high_i in high_minus_periods:
            _plot_pct_high(ax, high_i, df, price_col)
        for low_i in low_plus_periods:
            _plot_pct_low(ax, low_i, df, price_col)
        plt.show()

        if taa_mv is not None and saa_mv is not None:
            taa_mv = taa_mv.rename(columns = {'mv':'taa'})
            saa_mv = saa_mv.rename(columns = {'mv':'saa'})
            df = saa_mv[['saa']].join(taa_mv['taa'])
            df = (df / df.iloc[0])
            df['taa/saa'] = df['taa'] / df['saa']
            fig, ax = plt.subplots(figsize= [20,12])
            plt.plot(df.index, df['taa/saa'], label = 'taa/saa', linewidth=2.0)
            plt.legend(fontsize=20 ,loc = 'upper left')
            plt.title(f'taa / ssa mv ', fontsize=30)
            for high_i in high_minus_periods:
                _plot_dif(ax, high_i, df, False)
            for low_i in low_plus_periods:
                _plot_dif(ax, low_i, df, True)
            plt.show()

    @staticmethod
    def plot_saa_rebalance_on_mv(asset_mv:pd.DataFrame,
                                rebalance_date:list,
                                MinActionAmtDiff:float,
                                annual_ret:float,
                                mdd:float,
                                ret_over_mdd:float):
        p = asset_mv['mv'].plot.line(figsize=(12,9), color = 'dodgerblue')
        m = MinActionAmtDiff
        annual_ret = round(annual_ret,4)
        mdd = round(mdd,4)
        ret_over_mdd=round(ret_over_mdd,4)
        t = plt.title(f'market value with AmtDiff {m} annual_ret {annual_ret} mdd {mdd} ret_over_mdd {ret_over_mdd} ', fontsize=20)
        for d, r in asset_mv.loc[rebalance_date,:].iterrows():
            pl.scatter(x=d, y=r.mv, c='r',s=50)
