from .Detection import Detection
import pandas as pd
#def Detection2(data_pre_all,outbreak_before,outbreak_after,pvalue_cusum_k):
#	Detection={};recent_data={}
#	for i,j in zip(range(len(range(outbreak_before,outbreak_after-3))),range(outbreak_before,outbreak_after-3)):
        #     data_pre=np.append(aba[:j],ARIMA_GRNN_data[i])
	#	Detection3(data_pre_all[i][:outbreak_after+1],pvalue_cusum_k=pvalue_cusum_k,name=str(j))
		#Detection[str(j)]=DT1;recent_data[str(j)]=RT1
#	df=pd.DataFrame.from_dict(Detection, orient='index')
#	print(df.T)
#	df.T.to_csv("PredictionDetection_output.csv")
#	df1=pd.DataFrame.from_dict(recent_data, orient='index')
	#print(df1.T)
#	df1.T.to_csv("PredictionRecentOutbreak_output.csv")
def _last(ts,detection_result):
    detection_result.sort();_last=[]
    for i in range(len(ts)-5,len(ts)):
        for j in range(len(detection_result)):
            if i==detection_result[j]-1:
                _last.append(ts.index[i].strftime("%Y-%m-%d"))
                print(ts.index[i].strftime("%Y-%m-%d"))
    return _last
def Detection2(data,pvalue_cusum_k,name):
    MK, Pettitt, BUT, SNHT, CUSUM_Test, EWMA_Test, Pvalue_CUSUM_Test = \
        Detection(data=data, pvalue_cusum_k=pvalue_cusum_k)
    print(CUSUM_Test)
    #print("Method 6: EWMA \n")
    print(EWMA_Test)
    MK=_last(data,MK)
    Pettitt=_last(data,[Pettitt])
    BUT=_last(data,[BUT])
    SNHT=_last(data,[SNHT])
    CUSUM_Test = CUSUM_Test[0]['violation-points'][1]
    CUSUM_Test= _last(data,CUSUM_Test)
    EWMA_Test = EWMA_Test[0]['violation-points'][1]
    EWMA_Test= _last(data,EWMA_Test)
    Pvalue_CUSUM_Test= _last(data,Pvalue_CUSUM_Test)   
    All_detection = [MK, Pettitt, BUT, SNHT, CUSUM_Test, EWMA_Test, Pvalue_CUSUM_Test]
    All_detection_name = ['Mann-Kendall', 'Pettitt', 'Buishand_U_Test ', 'Standard Normal Homogeinity Test', 'CUSUM', 'EWMA', 'P value-CUSUM']
    dic=dict(zip(All_detection_name,All_detection))
    #pd.Series(dic).to_csv("./{}_Last_Outbreaks_detected_by_seven_detection_methods.csv".format(name))
    pd.Series(dic).to_csv('Detected_recent_outbreak_signal.txt', sep='\t', index=True)
    print("\n")
    print("{} The last Outbreaks detection result file saved successfully\n".format(name))
