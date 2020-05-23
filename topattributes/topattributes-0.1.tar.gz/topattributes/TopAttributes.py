import pandas as pd

class Topvariables():
    def __init__(self, data, dep):
        self.data = data
        self.dep = dep
    
    def correlation(self, ):
        
        columns = list(self.data.columns)
        corr_list = [[],[]]
        for var in columns:
            if var != self.dep:
                corr_list = corr_list.append([var, data[dep].corr(data[var])])
        print(corr_list)
        return corr_list

        
        