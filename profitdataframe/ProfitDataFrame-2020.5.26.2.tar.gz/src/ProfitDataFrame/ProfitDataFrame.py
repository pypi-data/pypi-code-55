#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import numpy as np


class Profitdataframe(pd.DataFrame):
    '''
    it's a package for myself to do somethings in ELT automatically。
    此包构建的目的是为了在EDA过程中自动化处理一些问题
    目前写了几个方法：
    q_info 方法是对原df.info()的重构。返回一个DataFrame,包含原表的列名、各列总计数目、非空、空、空率、字段类型、前五预览
    q_view 方法将原本pd.plotting.scatter_matrix(df) 缩写,即查看各列间的多重共线性
    q_tips 方法塞入了一些常用的命令，方便复制修改（好吧我承认是为了考试写的这个方法）
    '''
    
    def q_info(self):
        '''
        it's a functhon which make a info with null_percent infos and traditional df.info()
        正在改进
        2020/5/26 profit q_info to suit whose index does not begins with 0
        '''
        ind = self.index
        col = self.columns
        ind_len = len(ind)
        col_len = len(col)
        df = pd.DataFrame(columns = ['total_count',
                                     'non_null_count',
                                     'null_count',
                                     'null_percent',
                                     'ddtype',
                                     '5th_view',])
        for i in col:
            the5th = ','.join([str(self[i][self.index[j]]) for j in range(5)])
            value = {'total_count':ind_len,
                     'non_null_count':self[i].count(),
                     'null_count':self[i].isnull().sum(),
                     'null_percent':self[i].isnull().sum()/ind_len,
                     'ddtype':self[i].dtype,
                     '5th_view':the5th
                    }
            temp = pd.Series(value,name = i)
            df.loc[i] =temp
        return df

    def q_view(self):
        pd.plotting.scatter_matrix(self)
        
    def q_tips(self,code = 0):
        if code == 0:
            print(r'code menu is online','code=0 means find this menu',
                 r'code = 1 means find shell for active-out',
                 r'code = 2 means find shell for wrongs in plot',sep = '\n')
        if code == 1 :
            print(r"from IPython.core.interactiveshell import InteractiveShell",
                  r"InteractiveShell.ast_node_interactivity = 'all'"
                 ,sep = '\n')
        if code == 2 :
            print(r"# 解决坐标轴刻度负号乱码 plt.rcParams['axes.unicode_minus'] = False",
                  r"# 解决中文乱码问题(上) plt.rcParams['font.sans-serif'] = ['Simhei']",
                  r"解决中文乱码问题(下) plt.rcParams[‘font.family’] = 'Arial Unicode MS'"
            ,sep = '/n')

