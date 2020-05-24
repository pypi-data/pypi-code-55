#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import accuracy_score



#dataset = pd.read_csv("C:/Users/Istiak/Desktop/Research/iris.csv")

def Classifiers(dataset):
    X = dataset.drop('classlabel', axis=1)
    y = dataset['classlabel']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    classifier = DecisionTreeClassifier()
    classifier.fit(X_train, y_train)
    y_pred_class = classifier.predict(X_test)
    accuracy_class = accuracy_score(y_test, y_pred_class)
    print('Outcomes from first model: ',y_pred_class)
    
    return y_pred_class, accuracy_class
    
def Regressors(dataset):
    
    X = dataset.drop('classlabel', axis=1)
    y = dataset['classlabel']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=8)
    regressor = DecisionTreeRegressor()
    regressor.fit(X_train, y_train)
    y_pred_reg = regressor.predict(X_test)
    accuracy_reg = accuracy_score(y_test, y_pred_reg, normalize=True)
    y_pred_reg = y_pred_reg.astype(int)
    print('Outcomes from second model: ',y_pred_reg)
    return y_pred_reg, accuracy_reg

#classifier = Classifiers(dataset) 
#regressor = Regressors(dataset)

def Argumentation(classifier, regressor):
    
    c1 = classifier[0]
    c2 = classifier[1]
    r1 = regressor[0]
    r2 = regressor[1]
    
    comp = (c1==r1)
    ln = c1.size
    lnr = r1.size
    #print(comp)
    for cmp in comp:
        if cmp == True:
            print('')
        else:
            if c2>r2:
                for i in range(0,ln,1):
                    if c1[i]!=r1[i]:
                        print(c1[i],'Attack-->', r1[i])
                        if c2>0.5:
                            print('Accepted Argument: ', c1[i])
                        elif c2<0.5:
                            print('Unaccepted Argument: ',c1[i])
                        elif c2==0.5:
                            print('Undefined Argument: ',c1[i])
                    else:
                        print('No Attack')
                break
                
            elif r2>c2:
                for i in range(0,ln,1):
                    if r1[i]!=c1[i]:
                        print(r1[i],'Attack-->', c1[i])
                        if c2>0.5:
                            print('Accepted Argument: ', r1[i])
                        elif c2<0.5:
                            print('Unaccepted Argument: ',r1[i])
                        elif c2==0.5:
                            print('Undefined Argument: ',r1[i])
                    else:
                        print('No Attack')
                break
                
            elif c2==r2:
                for i in range(0,ln,1):
                    if c1[i]!=r1[i]:
                        print(c1[i],'Attack-->', r1[i])
                        if c2>0.5:
                            print('Accepted Argument: ', c1[i])
                        elif c2<0.5:
                            print('Unaccepted Argument: ',c1[i])
                        elif c2==0.5:
                            print('Undefined Argument: ',c1[i])
                    else:
                        print('No Attack')
                break
    return 

def PlotGraph(classifier, regressor):
    print('----Graphical View----')
    c1 = classifier[0]
    r1 = regressor[0]
   
    plt.figure(1)
    plt.plot(c1,"b-*",label='First model')
    plt.legend(loc='best')
    
    
    plt.figure(2)
    plt.plot(r1,"r-h", label='Second model')
    plt.legend(loc='best')
    
    
    plt.figure(3)
    plt.plot(c1,"b-*", label='First model')
    plt.plot(r1,"r-h", label='Second model')
    plt.legend(loc='best')
    plt.show() 

#Argumentation(classifier, regressor)
#PlotGraph(classifier, regressor)


# In[ ]:




