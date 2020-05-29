from neupy import algorithms
import numpy as np
from sklearn import datasets, preprocessing
from sklearn.model_selection import train_test_split

def GRNN_Predict_Model(X,Y,std=0.02):
    scaler = preprocessing.MinMaxScaler()
    arima_values=scaler.fit_transform(X)
    origin_values=scaler.fit_transform(Y.reshape((-1, 1)))
    arima=arima_values[:len(arima_values)-4]
    origin=origin_values[:len(origin_values)-4]
    x_train, x_test, y_train,y_test = train_test_split(arima,origin,train_size = 0.7,random_state=0)
    nw = algorithms.GRNN(std=std, verbose=False)
    nw.train(x_train, y_train)
    # y_Predict = nw.predict(x_test)
    GRNN_Predict = nw.predict(arima_values)
    GRNN_Predict[np.isnan(GRNN_Predict)] = 0 # If NA is encountered, replace it with 0
    #print(GRNN_Predict)
    origin_values_inverse=scaler.inverse_transform(origin_values)
    GRNN_Predict_inverse =scaler.inverse_transform(GRNN_Predict )
    return GRNN_Predict_inverse
