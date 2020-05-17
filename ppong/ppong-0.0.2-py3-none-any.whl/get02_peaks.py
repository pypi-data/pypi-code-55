from rohan.global_imports import *
from rohan.dandage.io_dict import read_dict,to_dict
def get_annot_rallies(df):
    from scipy.signal import find_peaks
    df1=df.groupby('time (ms)').agg({'db (log-scale)':[np.mean,np.std]})
    df1.columns=coltuples2str(df1.columns)
    df1=df1.reset_index()
    peak_positions,peak_heights=find_peaks(df1['db (log-scale) mean'],
                                                    height=[-50,0],
                                                    threshold=-50,
                                                    distance=5,
                                                    width=[3,40]
                        )
    df1.loc[peak_positions,'db (log-scale) mean peak']=peak_heights['peak_heights']
    times=df1.loc[~df1['db (log-scale) mean peak'].isnull(),'time (ms)']
    df1.loc[~df1['db (log-scale) mean peak'].isnull(),'db (log-scale) mean peak delay']=np.insert(np.diff(times),0,0)
    df1.loc[~df1['db (log-scale) mean peak'].isnull(),'rally begin']=df1.loc[~df1['db (log-scale) mean peak'].isnull(),'db (log-scale) mean peak delay']>1000
    df1.loc[~df1['db (log-scale) mean peak'].isnull(),'rally #']=df1.loc[~df1['db (log-scale) mean peak'].isnull(),'rally begin'].cumsum().replace(False,0)
    return df1

def get01_date2dpeakp(cfg,date2dspectrogramp,date2dpeakp):
    # dn2dp=cfg['date2pathm4ap']
    dn2dp=read_dict(date2dspectrogramp)
    dn2outp={}
    for k in dn2dp:
        outpre=f"{dirname(date2dpeakp)}/{k}"
        dn2outp[k]=f'{outpre}_small.pqt'
        if not exists(dn2outp[k]):
            df1=read_table(f"{dirname(date2dspectrogramp)}/{k}.pqt")
            df2=get_annot_rallies(df1)
            to_table(df2,f'{outpre}.pqt')
            to_table(df2.dropna(subset=['db (log-scale) mean peak']),dn2outp[k])
    to_dict(dn2outp,date2dpeakp)
    

    