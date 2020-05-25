#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys, os
sys.path.insert(0, os.path.abspath(r'..\..\..\qilum'))
sys.path.insert(0, os.path.abspath('qilum'))
# sys.path.insert(0, r'D:\Projects\Jupyter\qilum')
import qilum.stats as qs
import numpy as np
import numba as nb
import scipy.stats 
from contextlib import suppress


# In[2]:


def test_f_max():
    """test f_max function: for a serie of values array ys and integer N,
    separate yz in N intervals and return the max of ys for each interval""" 
    # input
    xs = np.linspace(-6,6, 101)
    ys = 3.*np.exp(-np.square(xs)/10.)

    # calcul
    xs_inter, ys_inter = qs.f_max(xs, ys, 10)    
    
    for i in range(xs.size):
        j = np.searchsorted(xs_inter, xs[i], side='right')-1 
        if j>ys_inter.size-1: 
            j = ys_inter.size-1    
        if not ys[i] <= ys_inter[j]:
            print(i,j,xs[i],xs_inter[j],ys[i], ys_inter[j],ys[i] <= ys_inter[j])
            assert ys[i] <= ys_inter[j]
    


# In[3]:


def test_walker_decomposition():
    """test f_walker : Walker decomposition: 
    given N probabilities , return a series of N boxes of value mean(probabilities) 
    with 2 indices in each"""

    # calcul
    probabilities = np.array([1,2,3,4,3.5], dtype=np.float64)
    P0, a = qs.f_walker(probabilities)

    P0_c= [0.37037037, 0.74074074, 0.         ,0.88888889, 0.40740741]
    a_c= [4, 4, 2, 2, 3]

    np.testing.assert_almost_equal(P0, P0_c)
    np.testing.assert_equal(a, a_c)


# In[4]:


def test_Dist_walker():
    """Compare Dist_walker vs scipy.stats.rv_discrete"""
    np.random.seed(12345)
    
    # input and calculation
    values = np.array([0, 10, 2])
    probabilities = np.array([0.2, 0.5, 0.3])
    scipy_discrete = scipy.stats.rv_discrete(values=(values, probabilities))
    walker = qs.Dist_walker(probabilities, values)

    # histogram vs pmf
    rans = walker.rvs(size=100000)
    hist, bins = np.histogram(rans, bins = np.linspace(-0.5,10.5, 12))
    bins = 0.5*(bins[:-1] + bins[1:])
    hist = hist/(hist.sum()*(bins[1]-bins[0]))
    pmf = walker.pmf(bins.astype(int))
    np.testing.assert_almost_equal(hist, pmf, decimal=3)
        

    #  cumulative: walker   vs scipy.stats.rv_discrete  
    xs = np.linspace(-20,20,4001)
    ys = walker.cdf(xs)
    zs = scipy_discrete.cdf(xs)
    np.testing.assert_almost_equal(ys, zs, decimal=3)


    #  ppf: walker   vs scipy.stats.rv_discrete  
    ys = np.linspace(0.001,1,1001)
    xs_ppf = walker.ppf(ys)
    zs_ppf = scipy_discrete.ppf(ys)
    np.testing.assert_almost_equal(xs_ppf, zs_ppf, decimal=7)


# In[5]:


def f_hist(*args, bins, density=True):    
    """helper function"""
    hist, bins = np.histogram(args, bins=bins, density=density)
    bins = (bins[1:]+bins[:-1])/2.
    return hist, bins

def f_test_histogram_cumulative(dist, NMC): 

    np.random.seed(123456)
    
    # ran x
    rans = dist.rvs(NMC)    
    hist, bins = f_hist(rans, bins=100)
    try:
        factor = dist.F_tot()
    except:
        index = np.argmax(hist)
        x_max = bins[index]        
        factor = dist.f(x_max)/hist[index]
    hist = hist*factor
    ys = dist.f(bins)
    np.testing.assert_almost_equal(hist, ys, decimal=2)
    ys_pdf = dist.pdf(bins)*factor
    np.testing.assert_almost_equal(ys, ys_pdf, decimal=5)

#     plt.plot(bins, hist, color= 'pink', linewidth=8, label='histo')
#     plt.plot(bins,ys, color= 'green', linewidth=3, label='f(x)')
#     plt.plot(bins,ys_pdf, color= 'black', linewidth=1, label='pdf(x)*F_tot)')
#     plt.legend(loc='upper left')
#     plt.title('ran ' + dist.name())


    # Cumulative
    # calculate approximate 
    cum = qs.f_cumulative(bins,ys)
    cum /= cum[-1]
    bins = bins[1:]
    ys1 = dist.cdf(bins)
    ys = ys1/ys1[-1]
    np.testing.assert_almost_equal(cum, ys, decimal=3)
#     print('bins=', cum )
#     print('bins=', ys)
#     print('bins=', cum - ys)
#     plt.plot(bins, cum - ys)        
#     plt.legend(loc='upper left')
#     plt.title('cumulative ' + dist.name())    
#     plt.show()

def test_Dist_scale():
    # scipy dist
    dist_exp = scipy.stats.expon()    
    # scale scipy dist with negative scale_x and multiplicative factor scale_y
    dist = qs.Dist_scale(dist_exp, loc_x=5, scale_x=-1, scale_y=2)
    # plot histogram and cumulative
    xs = np.linspace(-10, 15, 10000)
    f_test_histogram_cumulative(dist, 10000000)

def test_Dist_sum():
    """test for Sum of distributions """

    norm1  = qs.Dist_scale(scipy.stats.norm(0,1),loc_x=-1, scale_x=-1, scale_y=2, name='Norm1')
    norm2 = qs.Dist_scale(scipy.stats.norm(2,1),loc_x= -1, scale_x= 1, scale_y=2, name='Norm2')

    # sum of the distributions
    dist_sum = qs.Dist_sum([norm1, norm2]); 

    # plot histogram and cumulative
    xs = np.linspace(-20,20, 100001)
    f_test_histogram_cumulative(dist_sum, 10000000)

def test_Dist_reject():
    """
    1. create a function f_sum(x) above the function f_f(x). The f_sum is defined on three intervals.
    2. create a sum of the known distributions for each part of f_sum function
    3. create the Dist_rejection distribution using this sum and the original f_f(x) function        
    """
    def f_f(xs):
        # gaussian
        return 3.*np.exp(-np.square(xs)/10.)

    # 1.create a function f_sum(x) above the function f_f(x).
    #   f_sum(x) = y0*exp(+a*x)  if x_min < x 
    #   f_sum(x) = step function if x_min < x <= x_max 
    #   f_sum(x) = y0*exp(-a*x)  if x_max < x               
    xs = np.linspace(-5,5, 1001)
    ys = f_f(xs)    
    xs_inter, ys_inter = qs.f_max(xs, ys, 6)    
    ys_inter *= 1.2 # just to be sure that our step function >= f_f() 
    # histogram distribution with the step function
    hist_dist = scipy.stats.rv_histogram((ys_inter, xs_inter))
    # scale this diribution
    cumulative = ((np.roll(xs_inter,-1)-xs_inter)[:-1]*ys_inter).sum()
    step = qs.Dist_scale(hist_dist, scale_y = cumulative)

    # exponential distribution at the left and right of the step distribution
    exp_left  = qs.Dist_scale(scipy.stats.expon(),loc_x=xs_inter[-1], scale_x=1, scale_y=ys_inter[-1], name='Exp+')
    exp_right = qs.Dist_scale(scipy.stats.expon(),loc_x=xs_inter[0]-1e-10, scale_x=-1,scale_y=ys_inter[0], name='Exp-')

    # 2. create a sum of the known distributions for each part of f2 function
    dist_sum    = qs.Dist_sum([exp_left, step, exp_right]) 
    # 3. create the Dist_rejection distribution using this sum and the original f_f(x) function        
    dist_reject = qs.Dist_reject(dist_sum, f_f)

    # test result with the normal distribution hypothesis since f_f is normal
    k2, p = scipy.stats.normaltest(dist_reject.rvs(1000000))
    assert(p > 1e-3)

def test_Dist_cubic_spline():
    # test function: gaussian
    def f_f(xs):
        return 3.*np.exp(-np.square(xs)/10.)

    # initialize class
    x = np.linspace(-12, 12, 51)
    y = f_f(x)  
    dist_cs = qs.Dist_cubicSpline(x, y, N_cs=1000)

    # test result with the normal distribution hypothesis since f_f is normal
    k2, p = scipy.stats.normaltest(dist_cs.rvs(1000000))    
    assert(p > 1e-3)


# In[6]:


# test_f_max()
# test_walker_decomposition()
# test_Dist_walker()        
# test_Dist_scale()    
# test_Dist_sum()
# test_Dist_reject()   
# test_Dist_cubic_spline()            


# In[ ]:




