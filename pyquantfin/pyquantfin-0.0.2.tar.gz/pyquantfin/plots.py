import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#from . import SAA

#def plot_frontier(r:'arr', covar:'arr2d', ax=None):
#    noa = len(r)
#    M = 1000
#    w = np.random.uniform(0,1,(M,noa))
#    w = w / w.sum(1).reshape(-1,1)
#    r = r.reshape(-1,1)
#    expected_return = np.dot(w,r)
#    variance = np.zeros(M)
#    for i in range(M):
#        variance[i] = np.dot(np.dot(w[i],covar),w[i].T)
#    
#    std = variance**(1/2)
#    
#    y_min = expected_return.min()
#    y_max = expected_return.max()
#    y = np.linspace(y_min, y_max, 100)
#    x = np.zeros_like(y)
#    for i in range(len(x)):
#        x[i] = SAA.mean_var_optimization(r,covar,y[i])[1] ** (1/2)
#    
#    if ax == None:
#        ax = plt.gca()
#    
#    ax.scatter(std * 100,expected_return * 100,alpha=0.5)
#    ax.scatter(x * 100,y * 100,marker='.',color='black')
#    ax.set_xlabel('Standard Deviation (%)')
#    ax.set_ylabel('Expected Return (%)')
#
#    ax.grid()

def _mark_position(prz:'arr', pos:'arr', x=[], marker='o', ax = None):
    k = 0
    p0 = pos[0]
    
    if x == []:
        x = np.arange(len(prz))

    if ax == None:
        fig,ax = plt.subplots(figsize=(10,5))

    for i,p1 in enumerate(pos[1:-1]):
        if p1!=p0 or i == len(pos)-3:
            if p0 == 0:
                color = 'grey'
                linewidth = 1.0
            else:
                color = 'red' if p0 > 0 else 'green'
                linewidth = 3.0
            ax.plot(x[k:i+1],prz[k:i+1],color=color,linewidth=linewidth,marker=marker)
            k = i
            p0 = pos[k]

    
def _mark_trade(prz:'arr', pos:'arr', x=[], marker='o', ax = None):
    offset = 2
    headlength = 8
    headwidth = 8
    width = 0
    
    if x == []:
        x = np.arange(len(prz))

    if ax == None:
        fig,ax = plt.subplots(figsize=(10,5))
        ax.plot(x, prz)
    
    for i in range(1,len(pos)):
        if pos[i-1] != pos[i]:
            y = prz[i]
            
            if pos[i] > 0:
                ax.annotate("", xy = (x[i], y*(1-offset/100)), xytext = (x[i], y*(1-2*offset/100)), arrowprops = dict(facecolor = "red", headlength = headlength, headwidth = headwidth, width = width))  
            elif pos[i] < 0:
                ax.annotate("", xy = (x[i], y*(1+offset/100)), xytext = (x[i], y*(1+2*offset/100)), arrowprops = dict(facecolor = "lightgreen", headlength = headlength, headwidth = headwidth, width = width))  
            else:   #pos[i] == 0
                if pos[i-1] < 0:
                    ax.annotate("", xy = (x[i], y*(1-offset/100)), xytext = (x[i], y*(1-2*offset/100)), arrowprops = dict(facecolor = "red", headlength = headlength, headwidth = headwidth, width = width))  
                else:
                    ax.annotate("", xy = (x[i], y*(1+offset/100)), xytext = (x[i], y*(1+2*offset/100)), arrowprops = dict(facecolor = "lightgreen", headlength = headlength, headwidth = headwidth, width = width))  


def mark(prz:'arr', pos:'arr', x = [], marker = 'o', mtype = 'trade'):
    if mtype == 'trade':
        _mark_trade(prz,pos,x,marker=marker)
    else:
        _mark_position(prz,pos,x,market=marker)
    
if __name__ == '__main__':
    prz = np.arange(100)
    pos = (np.random.uniform(0,1,100) > 0.5 ).astype(int)
    dates = [str(i) for i in range(100,200)]