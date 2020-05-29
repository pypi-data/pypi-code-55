from .Prediction import *
import re,os
from itertools import groupby
#from operator import itemgetter
import numpy as np
from .Detection import Detection
from .PredictionDetection import PredictionDetection
def Tran_time(data,list_a):
    list_a.sort()
    num=[]
    fun = lambda x: x[1]-x[0]
    for k, g in groupby(enumerate(list_a), fun):
        l1 = [j for i, j in g]    # A list of consecutive numbers
        if len(l1) > 1:
            scop = str(min(l1)) + '-' + str(max(l1))    # Concatenate consecutive number ranges with "-"
        else:
            scop = l1[0]
        num.append(scop)
    #print(num)
    b=[]
#     if len(list_a)>0:
#    if isinstance(data,np.ndarray):
#        data=pd.Series(data,index=pd.date_range("1/1/2014",periods=len(data),freq="D"))
    for i in num:
        if isinstance(i, str):
            scop_=i.split("-")
            scop_time=[]
            for j in scop_:
        #        if isinstance(data,np.ndarray):
        #            data=pd.Series(data,index=pd.date_range("1/1/2014",periods=len(data),freq="D"))
                    
                tmp=data.index[int(j)-1] 
                scop_time.append(tmp.strftime("%Y/%m/%d"))
            b.append(str(scop_time[0]) + '-' + str(scop_time[1]))
        if isinstance(i, int): 
#         print(i.split("-"))
            tmp=data.index[i-1]
            b.append(tmp.strftime("%Y/%m/%d"))
    return b
def Detection3(data,pvalue_cusum_k,name):
#    if not os.path.exists("./Outbreak_result"):
#        os.mkdir("./Outbreak_result")

    # data=read_data(file=file)
    MK, Pettitt, BUT, SNHT, CUSUM_Test, EWMA_Test, Pvalue_CUSUM_Test = \
        Detection(data=data, pvalue_cusum_k=pvalue_cusum_k)  # The data parameter in the Detection module can be a file path or a time series format
    #print("Method 5: CUSUM \n")
    print(CUSUM_Test)
    #print("Method 6: EWMA \n")
    print(EWMA_Test)
    MK=Tran_time(data,MK)
    Pettitt=Tran_time(data,[Pettitt])
    BUT=Tran_time(data,[BUT])
    SNHT=Tran_time(data,[SNHT])
    CUSUM_Test = CUSUM_Test[0]['violation-points'][1]
    CUSUM_Test=Tran_time(data,CUSUM_Test)
    EWMA_Test = EWMA_Test[0]['violation-points'][1]
    EWMA_Test=Tran_time(data,EWMA_Test)
    Pvalue_CUSUM_Test=Tran_time(data,Pvalue_CUSUM_Test)
    All_detection = [MK, Pettitt, BUT, SNHT, CUSUM_Test, EWMA_Test, Pvalue_CUSUM_Test]
    All_detection_name = ['Mann-Kendall', 'Pettitt', 'Buishand_U_Test ', 'Standard Normal Homogeinity Test', 'CUSUM', 'EWMA', 'P value-CUSUM']
    dic=dict(zip(All_detection_name,All_detection))
#    if not os.path.exists("./Outbreak_result/History_records/"):
#        os.mkdir("./Outbreak_result/History_records/")
    #pd.Series(dic).to_csv("./{}_Outbreaks_detected_by_seven_detection_methods.csv".format(name))
    pd.Series(dic).to_csv('Detected_all_outbreak_signal.txt', sep='\t', index=True)
    print("\n")
    print("{} Outbreaks detection result file saved successfully\n".format(name)) 
#    return Detection_value,recent_data
