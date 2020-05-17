from rohan.global_imports import *
from rohan.dandage.io_dict import read_dict,to_dict

def get01_dpeaks_raw(date2dpeakp,dpeaks_rawp):
    date2dpeakp=read_dict(date2dpeakp)
    df1=pd.concat({k: read_table(date2dpeakp[k]) for k in date2dpeakp},names=['date'],axis=0).reset_index()
    to_table(df1,dpeaks_rawp)
        
def get02_dstats(dpeaks_rawp,dstatsp):
    df01=read_table(dpeaks_rawp)
    df1=df01.groupby(['date','rally #']).agg({
                                          'time (ms)':[len,np.mean,lambda x: np.max(x)-np.min(x)],
                                          'db (log-scale) mean':[np.mean],
                                          })
    df1.columns=coltuples2str(df1.columns)
    df1=df1.reset_index()
    rename=dict(zip(['date',
     'rally #',
     'time (ms) len',
     'time (ms) mean',
     'time (ms) <lambda_0>',
     'db (log-scale) mean mean'],
     ['date',
     'rally #',
     'bounces all',
     'time (ms) mean',
     'rally duration',
     'loudness (db)']))
    df2=df1.rename(columns=rename)
    df2['shots']=df2['bounces all']/2
    df2['rally count']=df2['shots']/2
    df2['rally speed']=df2['rally count']/df2['rally duration']
    df2['rally speed']=df2['rally speed'].replace([np.inf,-np.inf],np.nan)
    df2['date']=df2['date'].apply(int)
    
    ds=df2['date'].drop_duplicates().sort_values()
    df=pd.DataFrame(ds)
    df.index=range(len(df))
    from datetime import datetime
    df['day gap']=df.apply(lambda x: (datetime.strptime(str(x['date']), '%y%m%d')-datetime.strptime(str(df.loc[x.name-1 if x.name!=0 else 0,'date']), '%y%m%d')).days ,axis=1)
    # df
    df['day #']=df['day gap'].cumsum()
    df['date']=df['date'].apply(int)
    df2=df2.merge(df,on='date',how='left')
    
    to_table(df2,dstatsp)
    
