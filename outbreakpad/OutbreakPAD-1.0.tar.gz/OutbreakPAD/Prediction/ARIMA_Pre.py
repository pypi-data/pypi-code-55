import numpy as np
from statsmodels.tsa.arima_model import ARIMA
import matplotlib.pylab as plt
import pandas as pd
from .ARIMA_Find_Parameter import *
def ARIMA_Pre(data,p,d,q):
    print("running ARIMA model !!!")
    size=len(data)
    X = data[:size].values
    X = np.array(X, dtype=np.float64)
    # size = int(len(X) * 0.66)
    train, test = X[0:size-4], X[size-4:len(X)]
    history = [x for x in train]
#    print(history)
    #results = sm.tsa.arma_order_select_ic(train, ic=['aic', 'bic'], trend='nc', max_ar=8, max_ma=8)
    
    #p, q = p_q_Parameter(train)
    predictions = list()
#    print(history)
    for t in range(len(test)):
        model = ARIMA(history, order=(p,d,q))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
#        print('predicted=%f, expected=%f' %(yhat, obs))
    bk_pre=np.append(train,predictions)
    bk=np.append(train,test)
    return bk_pre
