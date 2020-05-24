import numpy as np
import pandas as pd

def boll(prz:'arr', N = 20, offset = 2, shft = True, frame = False):
    df = pd.DataFrame()
    df['prz'] = prz
    df['mid'] = df.prz.rolling(N).mean().shift(int(shft))
    df['std'] = df.prz.rolling(N).std().shift(int(shft))
    df['upper'] = df['mid'] + offset * df['std']
    df['lower'] = df['mid'] - offset * df['std']
    if frame:
        return df
    else:
        return {c:df[c].values for c in df}

def don(prz:'arr', N = 20, shft = True, frame = False):    
    df = pd.DataFrame()
    df['prz'] = prz
    df['upper'] = df.prz.rolling(N).max().shift(int(shft))
    df['lower'] = df.prz.rolling(N).min().shift(int(shft))
    df['mid'] = (df.upper + df.lower)/2
    if frame:
        return df
    else:
        return {c:v.values for c,v in df.iteritems()}

def ma(prz:'arr', *args, shft = True, frame = False):
    s = pd.Series(prz)
    d = {'ma{}'.format(i): s.rolling(i).mean().shift(int(shft)).values for i in args}
    d['prz'] = prz
    if frame:
        return pd.DataFrame(d)
    else:
        return d
    
def rsi(prz:'arr', N = 20, shft = True, frame = False):
    df = pd.DataFrame()
    df['prz'] = prz
    df['chg'] = df.prz.diff()
    df['chg_up'] = np.maximum(df.chg.values, 0)
    df['chg_down'] = np.abs(np.minimum(df.chg.values, 0))
    df['A'] = df.chg_up.rolling(N - 1).sum()
    df['B'] = df.chg_down.rolling(N - 1).sum()
    df['rsi'] = df.A / (df.A + df.B) * 100
    df['rsi'] = df.rsi.shift(int(shft))
    if frame:
        return df
    else:
        return {'prz': prz, 'rsi': df.rsi.values}
    
def macd(prz:'arr', N1 = 12, N2 = 26, N3 = 9, shft = True, frame = False):
    df = pd.DataFrame()
    df['prz'] = prz
    df['ma1'] = df.prz.rolling(N1).mean().shift(int(shft))
    df['ma2'] = df.prz.rolling(N2).mean().shift(int(shft))
    df['dif'] = df.ma1 - df.ma2
    df['dea'] = df.dif.rolling(N3).mean().shift(int(shft))
    df['macd'] = 2 * (df.dif - df.dea)
    if frame:
        return df
    else:
        return {c:v.values for c,v in df.iteritems()}
    
def mom(prz:'arr', *args, frame = False):
    df = pd.DataFrame()
    df['prz'] = prz
    for i in args:
        df['mom' + str(i)] = df.prz.shift(i)
    if frame:
        return df
    else:
        return {c:v.values for c,v in df.iteritems()}
    
def cci(holc, N, shft = True, frame = False):
    df = pd.DataFrame()
    df['high'] = holc['high']
    df['open'] = holc['open']
    df['low'] = holc['low']
    df['close'] = holc['close']
    df['TP'] = (df.high + df.low + df.close) / 3
    df['MA'] = df.TP.rolling(N).mean()
    df['MD'] = (df.TP - df.MA).abs().rolling(N).mean()
    df['cci'] = (df.TP - df.MA) / df.MD / 0.015
    if shft:
        df['cci'] = df.cci.shift()
    if frame:
        return df
    else:
        return {c:df[c].values for c in ['high','open','low','close','cci']}

def atr(holc, N, shft = True, frame = False):
    df = pd.DataFrame()
    df['high'] = holc['high']
    df['open'] = holc['open']
    df['low'] = holc['low']
    df['close'] = holc['close']
    df['close_p'] = df.close.shift()
    df['tr'] = np.maximum(np.maximum((df.high - df.low).values, (df.high - df.close_p).values),
                          (df.close_p - df.low).values)
    df['atr'] = df.tr.rolling(N).mean()
    if shft:
        df['tr'] = df.tr.shift()
        df['atr'] = df.atr.shift()
    if frame:
        return df
    else:
        return {c:df[c].values for c in ['high','open','low','close','tr','atr']}
    
def adx(holc, N, shft = True, frame = False):
    df = pd.DataFrame()
    df['high'] = holc['high']
    df['open'] = holc['open']
    df['low'] = holc['low']
    df['close'] = holc['close']
    df['close_p'] = df.close.shift()
    df['high_p'] = df.high.shift()
    df['low_p'] = df.low.shift()
    df['PDM'] = df.high - df.high_p
    df['MDM'] = df.low_p - df.low
    df['PDM_adj'] =  df.PDM.where(df.PDM > df.MDM, 0)
    df['PDM_adj'] =  df.PDM_adj.where(df.PDM_adj > 0, 0)
    df['MDM_adj'] =  df.MDM.where(df.MDM > df.PDM, 0)
    df['MDM_adj'] =  df.MDM_adj.where(df.MDM_adj > 0, 0)
    df['tr'] = atr(holc, N, shft = False)['tr']
    df['PDI'] = df.PDM_adj.rolling(N).mean() / df.tr.rolling(N).mean()
    df['MDI'] = df.MDM_adj.rolling(N).mean() / df.tr.rolling(N).mean()
    df['DX'] = 100 * (df.PDI - df.MDI).abs() / (df.PDI + df.MDI)
    df['ADX'] = df.DX.rolling(N).mean()
    if shft:
        df.DX = df.DX.shift()
        df.ADX = df.ADX.shift()
    if frame:
        return df
    else:
        return {c:df[c].values for c in ['high','open','low','close','DX','ADX']}
    