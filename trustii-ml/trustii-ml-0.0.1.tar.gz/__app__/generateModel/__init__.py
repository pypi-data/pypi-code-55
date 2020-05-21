import os
import numpy as np

class TrustiiAggregateModel:
    def __init__(self, models, alphaStar,score,mlType='regression'):
        self.models = models
        self.alphaStar = alphaStar
        self.score = score
        self.type = 'TRUSTII-AGGREGATE-MODEL-v0.1'
        self.mlType=mlType

    def predict(self, X):
        omega = X
        inputList = []
        for model in self.models:
            inputList.append(model.predict(X=omega))
        
        M = np.array(inputList)
        M = M.transpose()
        prediction = []
        for each in range(0,len(omega)):
            sum=0
            for i in range(0,len(self.models)):
                sum = sum + self.alphaStar[i]*M[each,i]
            prediction.append(sum[0])
        return prediction

