import numpy as np
from statsmodels.tsa.arima_model import ARIMA
import matplotlib.pylab as plt
from sklearn.metrics import mean_squared_error
import pandas as pd
from .GRNN_Predict_Model import GRNN_Predict_Model
from .read_data import read_data
from .ARIMA_Find_Parameter import *
import warnings
warnings.simplefilter("ignore")
def ARIMA_GRNN_Pre(data,p,d,q,std=0.02):
#    data=read_data(file)
    print("running ARIMA-GRNN model")
    size=len(data)
    X = data[:size].values
    X = np.array(X, dtype=np.float64)
    # size = int(len(X) * 0.66)
    train, test = X[0:size-4], X[size-4:len(X)]
    history = [x for x in train]
#    p,q=p_q_Parameter(train)
    predictions = list()
    # print(history)
    for t in range(len(test)):
        model = ARIMA(history, order=(p,0,q))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        print('predicted=%f, expected=%f' % (yhat, obs))
   ###################################################################
    bk_pre=np.append(train,predictions)
    bk=np.append(train,test)
#    input_data, output_data =bk_pre[:size-4],bk[:size-4]
    ARIMA_GRNN_data=GRNN_Predict_Model(bk_pre, bk,std=std)
#    print(ARIMA_GRNN_data)

    ################################################################
#    error = mean_squared_error(output_data,ARIMA_GRNN_data)
#    print('Test MSE: %.3f' % error)
#    plt.title("test part")
#    output_data=output_data[8:]
    ARIMA_GRNN_data=ARIMA_GRNN_data[len(bk)-4:]
#    plt.plot(output_data,color='green')
#    plt.plot(ARIMA_GRNN_data, color='red')
#    plt.show()
#    yeast_bk_pre=np.append(train,ARIMA_GRNN_data)
#    yeast_bk=np.append(train,test)
#    for i in range(len(ARIMA_GRNN_data)):
#        print('predicted=%f, expected=%f'%(ARIMA_GRNN_data[i], output_data[i]))
    return ARIMA_GRNN_data
