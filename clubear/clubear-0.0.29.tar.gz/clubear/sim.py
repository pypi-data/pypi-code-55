from .fun import ispump
from matplotlib import pyplot as plt
from sklearn.metrics import roc_auc_score

import IPython,os,time,copy,random
import pandas as pd
import numpy as np
import seaborn as sns
import warnings; warnings.filterwarnings("ignore")
import matplotlib.cm as cm
import scipy.stats as sps

class simulator(object):

    def demo():
        '''demo is used to demonstrate typical examples about this class.'''
        demostr = '''
import clubear as cb
#clubear.csv is generated by cb.manager.demo()
pm=cb.pump('clubear.csv')
pm.qlist=['age','height','logsales','price']
cb.model(pm).ols('logsales',tv=False)
'''
        print(demostr)
        
    def __init__(self):
        'Initialization: set beta0, subsize, and method'
        
        self.beta0=[1]*10
        self.subsize=1000
        self.method='ols'
        self.tab=[]

    def go(self):        
        '''go is used to pump out data'''
        if not isinstance(self.beta0,list): print('simulator.go: The input beta0 should be a list.'); return
        try: tmp=np.mean(self.beta0);
        except: print('simulator.go: The input beta0 must be numeric.'); return
        ncov=len(self.beta0)
        if not isinstance(self.subsize,int): print('simulator.go: The input ss should be an int.'); return
        if not isinstance(self.method,str): print('simulator.go: The input method should be a str.'); return
        self.method=self.method.strip()
        
        methods=['ols','logit','stats','table','mu','std','size','box']
        if self.method not in methods: print('simulator.go: Unknown method detected.'); return
        
        if self.method=='ols':
            X=np.random.normal(0,1,[self.subsize,ncov])
            X[:,0]=1
            MU=X.dot(self.beta0)        
            Y=MU+np.random.normal(0,1,self.subsize)   
            Y=Y.reshape([self.subsize,1])
            out=pd.DataFrame(np.hstack([X,Y]))
            heads=['X'+str(each) for each in range(ncov)]+['Y']
            out.columns=heads
            
        if self.method=='logit':
            X=np.random.normal(0,1,[self.subsize,ncov])
            X[:,0]=1
            MU=X.dot(self.beta0)        
            prob=np.exp(MU);prob=prob/(1+prob)
            Y=1*(np.random.uniform(0,1,self.subsize)<prob)
            Y=Y.reshape([self.subsize,1])
            out=pd.DataFrame(np.hstack([X,Y]))
            heads=['X'+str(each) for each in range(ncov)]+['Y']
            out.columns=heads
            
        if self.method=='stats':
            X=np.random.normal(0,1,[self.subsize,ncov])
            for j in range(ncov): X[:,j]=X[:,j]*np.sqrt(1+j)+self.beta0[j]
            out=pd.DataFrame(X)
            heads=['X'+str(each) for each in range(ncov)]
            out.columns=heads
                   
        if self.method in ['table','size']:
            if not isinstance(self.tab,list): print('simulagor.go: The tab input must be a list'); return
            flag=[1*isinstance(each,str) for each in self.tab]
            if np.min(flag)==0: print('simulator.go: Each element of tabl must be a str.'); return
            ncov=len(self.tab)
            
            X=np.zeros([self.subsize,ncov]).astype(str)
            for i in range(self.subsize):
                for j in range(ncov):
                    X[i,j]=random.choice(self.tab[j])
            heads=['X'+str(each) for each in range(ncov)]
            out=pd.DataFrame(X)                                    
            out.columns=heads
            
            results=[]
            for j in range(ncov):
                mystr=sorted(list(set(self.tab[j])))
                mycounts=[self.tab[j].count(each) for each in mystr]
                mycounts=mycounts/np.sum(mycounts)
                results.append([mystr,mycounts])
            self.Table=pd.Series(results,heads)
            
        if self.method in ['mu','std','box']:
            X=np.random.uniform(0,1,self.subsize)
            X=np.floor(X*10)+1;
            Y=np.random.normal(0,1,self.subsize)*np.sqrt(X)+X
            out=pd.DataFrame(list(zip(X,Y)))
            out.columns=['X','Y']
            self.Mu=list(range(1,ncov+1))
            self.Std=np.sqrt(self.Mu)
            
        return out
