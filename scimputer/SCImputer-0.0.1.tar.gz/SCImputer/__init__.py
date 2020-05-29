import csv
import os

def divide(path,row_number):
    with open(path,'r',newline='') as file:
        csvreader = csv.reader(file)
        a = next(csvreader)
        print(a)
        i = j = 1
        for row in csvreader:
            print(row)
            print(f'i is {i} , j is {j}')
            if i % row_number == 0:
                j += 1
                print(f"csv{j}生成成功")
            csv_path = os.path.join('/'.join(path.split('/')[:-1]),'result' +  str(j) + '.csv')
            print(csv_path)
            if not os.path.exists(csv_path):
                with open(csv_path, 'w', newline='') as file:
                    csvwriter = csv.writer(file)
                    csvwriter.writerow(['image_url'])
                    csvwriter.writerow(row)
                i += 1
            # 存在的时候就往里面添加
            else:
                with open(csv_path, 'a', newline='') as file:
                    csvwriter = csv.writer(file)
                    csvwriter.writerow(row)
                i += 1
import pandas as pd
import numpy as np
import sklearn
from sklearn.metrics import explained_variance_score, max_error, mean_squared_error, mean_squared_log_error, r2_score
from sklearn import preprocessing



def ravel_data(data):
    
    data=pd.read_csv(data,delimiter=",")
    data=np.array(data)
    data=np.ravel(data)
    (m,)=data.shape
    data=data.reshape(m,1)
    return data
def evaluate(n):#n为选取的算法数目
    algset={1:'raw_data',2:'mean',3:'median',4:'mode',5:'random',6:'I',7:'ISVD',8:'fastknn',9:'KNN',10:'NNM',11:'MF',12:'EM'}
    for i in range(1,n+2):
        algset[i]=ravel_data(data=algset[i]+'.csv')
    
    A=np.zeros((n+1,n+1))
    B=np.zeros((n+1,n+1))
    C=np.zeros((n+1,n+1))
    
    for i in range(1,n+2):
        for j in range(1,n+2):
            A[i-1][j-1]=r2_score(algset[i],algset[j])
            B[i-1][j-1]=mean_squared_error(algset[i],algset[j])
            C[i-1][j-1]=explained_variance_score(algset[i],algset[j])
    with open('r2_score.csv','wb'):
        np.savetxt('r2_score.csv',A,delimiter=',')
    with open('MSE.csv','wb'):
        np.savetxt('MSE.csv',B,delimiter=',')
    with open('EVS.csv','wb'):
        np.savetxt('EVS.csv',C,delimiter=',')
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
MSE = np.loadtxt('MSE.csv',delimiter=',')
EVS = np.loadtxt('evs.csv',delimiter=',')
r2_score = np.loadtxt('r2_score.csv',delimiter=',')
fig = plt.figure()
MSE_plot = sns.heatmap(MSE)
plt.show()
EVS_plot = sns.heatmap(EVS)
plt.show()
R2_plot = sns.heatmap(r2_score)
plt.show()
import csv
import pandas as pd
import numpy as np
import cloudpickle
from sklearn.preprocessing import Imputer
from csv import reader
import os
import impyute
from impyute.imputation.cs import buck_iterative
import fancyimpute
from fancyimpute import IterativeSVD, KNN, MatrixFactorization, NuclearNormMinimization,BiScaler
import time
from sklearn.impute._iterative import IterativeImputer



def mean_impute(data,result):#均值填补
    
    dataframe=pd.read_csv(data)
    imp = Imputer(missing_values='NaN',strategy='mean',axis=0)
    imp.fit(dataframe)
    data01 = imp.transform(dataframe)
    processed_data = pd.DataFrame(data01)
    processed_data.to_csv(result)


def random_impute(data,result):#插补随机值
    dataframe=pd.read_csv(data)
    dataframe=np.array(dataframe)
    data01=impyute.imputation.cs.random(dataframe)
    
    
    processed_data = pd.DataFrame(data01)
    processed_data.to_csv(result)
      

def mode_impute(data,result):#模式插补
    dataframe=pd.read_csv(data)
    dataframe=np.array(dataframe)
    data01=impyute.imputation.cs.mode(dataframe)
    processed_data = pd.DataFrame(data01)
    processed_data.to_csv(result)

        
        
def median_impute(data,result):#中位数插补
    dataframe=pd.read_csv(data)
    dataframe=np.array(dataframe)

    data01 =impyute.imputation.cs.median(dataframe) 
    processed_data = pd.DataFrame(data01)
    processed_data.to_csv(result)



def EM_impute(data,result,loop_number):#期望最大化插补
    dataframe=pd.read_csv(data)
    dataframe = np.array(dataframe)
    data01 = impyute.imputation.cs.em(dataframe,loops=loop_number)
    processed_data = pd.DataFrame(data01)
    processed_data.to_csv(result)

def fast_knn_impute(data,result,k,eps,p):#快速KNN插补
    dataframe=pd.read_csv(data)
    dataframe = np.array(dataframe)
    data01 = impyute.imputation.cs.fast_knn(dataframe,k=k,eps=eps,p=p)
    processed_data = pd.DataFrame(data01)    
    processed_data.to_csv(result)

def KNN_impute(data,result):
    dataframe=pd.read_csv(data)
    processed_data = KNN(k=4).fit_transform(dataframe)
    processed_data = pd.DataFrame(processed_data)
    processed_data.to_csv(result)


def IterativeImpute(data,result):
    dataframe=pd.read_csv(data)
    processed_data = IterativeImputer().fit_transform(dataframe)
    processed_data = pd.DataFrame(processed_data)
    processed_data.to_csv(result)

def IterativeSVD_Impute(data,result):
    dataframe=pd.read_csv(data)
    processed_data = IterativeSVD().fit_transform(dataframe)
    processed_data = pd.DataFrame(processed_data)
    processed_data.to_csv(result)

def MatrixFactorization_Impute(data,result):
    dataframe=pd.read_csv(data)
    processed_data = MatrixFactorization().fit_transform(dataframe)
    processed_data = pd.DataFrame(processed_data)
    processed_data.to_csv(result)

def NuclearNormMinimization_Impute(data,result):
    dataframe=pd.read_csv(data)
    processed_data = NuclearNormMinimization().fit_transform(dataframe)
    processed_data = pd.DataFrame(processed_data)
    processed_data.to_csv(result)
import numpy as np
import pandas as pd
from csv import reader
import sklearn
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn import neighbors
from sklearn.preprocessing import Imputer
from dask.dataframe.io import csv

def load_data(filename,gradient,init_rate,maxrate):#梯度缺失率处理
    data = pd.read_csv(filename)
    print(data.shape)#矩阵形状
    print(data)
    
    (row_number,column_number) = data.shape#一行测序数据的数目

    init = init_rate
    droprate = np.zeros((10))
    for i in range(1,10):
        if droprate[i-1] <= maxrate:
            droprate[i-1] = init + gradient*i
        else:continue
    print(droprate)
    NA_data=data.replace(0,np.nan)#将0值转换为nan，方便后面调用函数
    print(NA_data)
    for i in range(1,10):
        if droprate[i-1] != 0 :
            deleted_data=NA_data.dropna(thresh=column_number*(droprate[i-1]))#依照缺失率删除缺失过多的序列
            #processed_data = deleted_data.apply(lambda x: (x - np.min(x)) / (np.max(x)-np.min(x)),axis=0)#归一化处理
            with open('preprocessed_data'+str(i)+'.csv','wb') as dataFile:
                deleted_data.to_csv('preprocessed_data'+str(i)+'.csv')
           