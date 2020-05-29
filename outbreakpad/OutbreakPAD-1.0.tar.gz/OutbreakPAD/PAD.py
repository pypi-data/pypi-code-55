from .Detection2 import Detection2
from .Detection3 import Detection3
from .PredictionDetection import PredictionDetection
import matplotlib.pyplot as plt
import matplotlib as mpl
def PAD(ts,output,p=2,d=0,q=1,a=["ARIMA-GRNN","ARIMA"],std=0.02,pvalue_cusum_k=1.5):
        import datetime,os
        import numpy as np
        import pandas as pd
        time_start=datetime.datetime.now()
        if not os.path.exists(output):
                os.mkdir(output)

       # if not os.path.exists(output+"/History_records/"):
       #         os.mkdir(output+"/History_records/")
#        pwd=os.getcwd()  
        os.chdir(output)
        Detection3(data=ts,pvalue_cusum_k=pvalue_cusum_k,name="Origin")
        print("Detection Done !!!\n")
        print("Now we are using the {} model to predict.".format(a))
       # os.chdir(output)
#        if not os.path.exists(output+"/Prediction/"):
#                os.mkdir(output+"/Prediction/")
#        os.chdir(output+"/Prediction/")
        #print(type(ts))
        for i in range(1,5):
            ts.loc[ts.index[len(ts)-1]+1]=0
       # print(ts)
#        ts.loc['f1'] = 0;ts.loc['f2'] = 0;ts.loc['f3'] = 0;ts.loc['f4'] = 0
        data_pre_all=PredictionDetection(data=ts,p=2,d=0,q=1,std=std,a=a)
        print("Prediction Done !!!\n")
        Detection3(data=data_pre_all,pvalue_cusum_k=pvalue_cusum_k,name=a)
        Detection2(data=data_pre_all,pvalue_cusum_k=pvalue_cusum_k,name=a)
        #Detection2(data_pre_all=data_pre_all,outbreak_before=outbreak_before,outbreak_after=outbreak_after,pvalue_cusum_k=pvalue_cusum_k)
#        df=pd.read_csv("{}_Prediction_data.csv".format(a),index_col=0)
        #mpl.use('TkAgg')
        plt.cla()
        #from matplotlib.backends.backend_pdf import PdfPages
        #pdf = PdfPages('./{}_Prediction.pdf'.format(a))
       # data=df[len(df.index)-10:]
       # x=range(len(data.index))
       # plt.plot(range(len(data.index)),data.iloc[:,1].values,linestyle="--",label="outbreak_before_4D")
       # plt.plot(range(len(data.index)),data.iloc[:,2].values,linestyle="--",label="outbreak_before_3D")
       # plt.plot(range(len(data.index)),data.iloc[:,3].values,linestyle="--",label="outbreak_before_2D")
       # plt.plot(range(len(data.index)),data.iloc[:,4].values,linestyle="--",label="outbreak_before_1D")
       # plt.plot(range(len(data.index)),data.iloc[:,0].values,linestyle="-",color="blue",label="rawdata")
       # plt.xticks(x, data.index, rotation=45)
       # plt.margins(0.08)
       # plt.subplots_adjust(bottom=0.15)
       # plt.legend(loc='best')
       # plt.show()
       # plt.savefig(fname='./{}_Prediction.svg'.format(a),format="svg")
       
      
#        Detection2(data_pre_all=data_pre_all,outbreak_before=outbreak_before,outbreak_after=outbreak_after,pvalue_cusum_k=pvalue_cusum_k)
        #os.chdir(output)
        time_end=datetime.datetime.now()
        print('time cost',time_end-time_start)
	
