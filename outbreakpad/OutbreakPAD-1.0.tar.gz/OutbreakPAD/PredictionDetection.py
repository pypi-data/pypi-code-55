from .Detection import Detection
from .Prediction import outbreak_prediction
#from .pad import pad
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from matplotlib.pylab import rcParams
def PredictionDetection(data,p,d,q,std=0.02,a=["ARIMA-GRNN","ARIMA"]):
#  'std' is the best smoothing factor parameter for GRNN
   #####################################################    prediction   ####################################################
   
    if a=="ARIMA-GRNN":
        Prediction_data=outbreak_prediction(data=data,p=p,d=d,q=q,std=std,a="ARIMA-GRNN")
       
    if a=="ARIMA":
        #print("ARIMA MODEL")
        Prediction_data=outbreak_prediction(data=data,p=p,d=d,q=q,a="ARIMA")
    print(Prediction_data)
    
#    data_pre=np.append(data,Prediction_data)
    
#    print(data_pre_all)
       # df[str(j)]=data_pre
 #   df=pd.DataFrame()
 #   df.index=data.index[:len(df)]
 #   df.insert(0,"rawdata",list(data.values))
   # data=df[len(df.index)-21:]
   # x=range(len(data.index))
   # plt.plot(range(len(data.index)),data.iloc[:,1].values,"--",label="outbreak_before_4D")
   # plt.plot(range(len(data.index)),data.iloc[:,2].values,"--",label="outbreak_before_3D")
   # plt.plot(range(len(data.index)),data.iloc[:,3].values,"--",label="outbreak_before_2D")
   # plt.plot(range(len(data.index)),data.iloc[:,4].values,"--",label="outbreak_before_1D")
   # plt.plot(range(len(data.index)),data.iloc[:,0].values,color="blue",label="rawdata")
   # plt.xticks(x, data.index, rotation=45)
   # plt.margins(0.08)
   # plt.subplots_adjust(bottom=0.15)
   # plt.legend(loc='best')
   # plt.show()
 #   df.to_csv("./{}_Prediction_data.csv".format(a))       
    for i in range(1,5):
#     print(i)
         data.iloc[len(data)-i]=Prediction_data[4-i]
    plt.cla()
    plt.plot(data[:len(data)-4],color="blue")
    plt.plot(data[len(data)-5:],'--',color="red")
    plt.show()
    plt.savefig(fname='./Lineplot_case_nubmber.svg',format="svg")
    plt.cla()
    plt.plot(data[len(data)-20:len(data)-4],color="blue")
    plt.plot(data[len(data)-5:],'--',color="red")
    plt.show()
    plt.savefig(fname='./Lineplot_case_number_recent_20_day.svg',format="svg")

#    data[len(data)-4:].to_csv("./Predicted_case_number.csv".format(a)) 
    data[len(data)-4:].to_csv('./Predicted_case_number.txt', sep='\t', index=True)
    return data
