#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
from numba import jit
import scipy.interpolate


# In[4]:


# generic functions
def f_np_array(arr):
    """
    utility function to tranform any input in a numpy array
    
    Parameters
    ----------
    arr : any value (np.array, list, tuple, single value)

    Returns
    -------
    sample: np.array
    
     Examples
    --------
    >>> import numpy as np
    >>> import qilum.stats as qs
    >>> qs.f_np_array(np.array([1,2,4]))
    array([1, 2, 4])
    >>> qs.f_np_array([4,3,5])
    array([4, 3, 5])
    >>> qs.f_np_array(8)
    array([8])
    """
    if arr is None:
        return None
    if not type(arr).__module__ == np.__name__:
        if not isinstance(arr, list):
            arr = [arr]
        arr = np.array(arr)
    return arr

def f_max(xs, ys, N):
    """maximun value ys in N intervals
    
    Parameters
    ----------
    xs : np.array 
        x values 
    ys : np.array
        y values 
    N : int 
        number of interval in the x range 

    Returns
    -------
    x_values : np.array
        interval values for x (size = N+1)            
    y_max_values: np.array  
        max of y on each interval (size = N) 
    
    Examples
    --------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> import qilum.stats as qs
    >>> # input
    >>> xs = np.linspace(-6,6, 1001)
    >>> ys = 3.*np.exp(-np.square(xs)/10.)
    >>>  
    >>> # calcul
    >>> xs_inter, ys_inter = qs.f_max(xs, ys, 10)    
    >>> 
    >>> # plot
    >>> plt.plot(xs, ys, label='f(x)')
    >>> plt.step(xs_inter[:-1], ys_inter, where='post',label='f_max(x)')
    >>> plt.title('N=10')
    >>> plt.legend()
    >>> plt.show()
        
    .. image:: /_static/f_max.jpg
    
    
    """
    xs = f_np_array(xs)
    ys = f_np_array(ys)
    return _f_max(xs, ys, N) 

@jit(nopython=True)
def _f_max(xs, ys, N):
    N_interval = int(ys.size/N)
    ys_inter = np.zeros(N, dtype=ys.dtype)
    xs_inter = np.zeros(N+1, dtype=ys.dtype)
    xs_inter[-1] = xs[-1]
    for i in range(N):
        start = i*N_interval
        end = start+N_interval
        if i == N-1:
            end = int(max(end, ys.size))
        ys_inter[i] = ys[start:end].max()
        xs_inter[i] = xs[start]
    return xs_inter,ys_inter

def f_cumulative(xs, ys, normalized = False):
    """cumulative calculation
    
    Parameters
    ----------
    xs : np.array 
        x values  
    ys : np.array
        y values. ys.size = xs.size-1 or ys.size = xs.size 
    normalized : bool
        if normalized=True, the cumulative is normalized to 1

    Returns
    -------
    cumulative_values : np.array
        array of size xs.size-1, not normalized            
    
    Examples
    --------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> import qilum.stats as qs
    >>> xs = np.linspace(-6,6, 1001)
    >>> ys = 3.*np.exp(-np.square(xs)/10.)
    >>> 
    >>> # calcul
    >>> # same size for xs and ys
    >>> cumulative1 = qs.f_cumulative(xs, ys, normalized=True)            
    >>> 
    >>> # xs are intervals where ys are constant: xs.size = ys.size+1 
    >>> ys = 0.5*(np.roll(ys,-1)+ys)[:-1]
    >>> cumulative2 = qs.f_cumulative(xs, ys, normalized=True)    
    >>> 
    >>> # plot
    >>> plt.plot(xs[1:], cumulative1, label='cumulative1',marker='.')
    >>> plt.plot(xs[1:], cumulative2, label='cumulative2')
    >>> plt.legend()
    >>> plt.show()
        
    .. image:: /_static/f_cumulative.jpg
    
    
    """
    ds = (np.roll(xs,-1)-xs)[:-1]
    if xs.size == ys.size:
        ys = 0.5*(np.roll(ys,-1)+ys)[:-1]
    cum = np.cumsum((ds*ys))
    if normalized:
        cum = cum/cum[-1]
    return cum


# In[5]:


# Walker
@jit(nopython=True, parallel=False)
def f_walker_alias(ps, k, a, P, b, L, H):
    # A.J. Walker, ACM Transaction on Mathematical Software 3 (1977) 253
    # http://www.damienloison.com/fast_algorithms/Potts/index.html
    # http://www.damienloison.com/fast_algorithms/Potts/create_Potts_walker.c
    max_L = L.size 
    max_H = H.size
    while max_L>0 and max_H>0:
        l=L[max_L-1]
        h=H[max_H-1]
        c=b[l]
        d=b[h]
        b[l]=0.
        b[h]=c+d
        max_L -= 1
        if b[h]<=0:
            max_H -= 1
        if b[h]<0: 
            L[max_L]=h
            max_L += 1
        a[l]=h
        P[l]=1.+k*c
    return P, a

def f_walker(probabilities):
    """given N probabilities , return a series of N boxes of value mean(probabilities) with 2 indices in each. 
    
    Parameters
    ----------
    probabilities : np.array
        an array of probability 

    Returns
    -------
    np.array, np.array
        probabilities(P), indices(a) 
    
    Examples
    ________
    
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> import qilum.stats as qs
    >>> 
    >>> # calcul
    >>> probabilities = np.array([1,2,3,4,3.5], dtype=np.float64)
    >>> P0, a = qs.f_walker(probabilities)
    >>> print("P0=",P0)
    P0= [0.37037037 0.74074074 0.         0.88888889 0.40740741]
    >>> print("a=",a)
    a= [4 4 2 2 3]
    >>> 
    >>> # figure
    >>> mean = probabilities.mean()
    >>> colors = np.array(['blue','black','pink','red','green'])
    >>> P1 = 1-P0        
    >>> P0 = P0*mean
    >>> P1 = P1*mean
    >>> ind = np.arange(P0.size)
    >>> print("P0*mean=",P0)
    P0*mean= [1.  2.  0.  2.4 1.1]
    >>> 
    >>> # plot
    >>> plt.figure(figsize=(10,4))
    >>> 
    >>> plt.subplot(1,2,1)
    >>> plt.ylim(0,4.3)
    >>> plt.bar(ind, probabilities, color=colors)
    >>> plt.axhline(y=mean)
    >>> plt.text(0, mean+0.1, 'mean', fontsize=15)
    >>> plt.title('probabilities', fontsize=18)
    >>> 
    >>> plt.subplot(1,2,2)
    >>> plt.ylim(0,4.3)
    >>> plt.bar(ind, P0, color=colors)
    >>> plt.bar(ind, P1, bottom=P0, color=colors[a])
    >>> plt.axhline(y=mean)
    >>> plt.text(0, mean+0.1, 'mean', fontsize=15)
    >>> plt.title('Walker decomposition', fontsize=18)
    >>>  
    >>> # calcul
    >>> xs_inter, ys_inter = qs.f_max(xs, ys, 10)    
    >>> plt.show()
        
    .. image:: /_static/f_walker.jpg
    
    References:
    
    .. [1] A.J. Walker, ACM Transaction on Mathematical Software 3 (1977) 253
    .. [2] http://www.damienloison.com/fast_algorithms/Potts/index.html
    .. [3] http://www.damienloison.com/fast_algorithms/Potts/create_Potts_walker.c
    
    """
    probabilities = f_np_array(probabilities)
    a = np.arange(0, probabilities.size, dtype = np.int64) 
    P = np.zeros(probabilities.size, dtype=np.float64)        
    ps = probabilities/probabilities.sum()
    # initialization
    k = ps.size
    b = ps -1./k
    L = np.where(b<0)[0]
    H = np.where(b>0)[0]
    return f_walker_alias(ps, k, a, P, b, L, H)


# In[6]:


# base class
class Dist_qilum:
    """Base class for any qilum distribution"""
    pass


# In[7]:


# Walter distribution

from numba import jit, njit
import numba as nb


@jit(nopython=True, parallel=True)
def f_walker_ran(ys, P, a, N, rans, indices):
    for i_ran in nb.prange(N):
        i = int(rans[i_ran]*ys.size)
        ran = rans[i_ran]*ys.size - i
        if ran >= P[i]:
            indices[i_ran] = a[i]
        else:
            indices[i_ran] = i
            
class Dist_walker(Dist_qilum):
    """
    Fast generator for discrete values using the Walker algorithm
    
    Parameters
    ----------
    probabilities : array_like
        an array of probability 
    values : array_like or None
        values corresponding to the probabilities. if 'None' values=arange(probabilities.size)

    Examples
    --------
    >>> import qilum.stats as qs
    >>> values = np.array([0, 10, 2])
    >>> probabilities = np.array([0.2, 0.5, 0.3])
    >>> walker = qs.Dist_walker(probabilities, values)
        
    .. image:: /_static/Dist_walker.jpg
        
    """
    def __init__(self, probabilities, values=None):        
        probabilities = f_np_array(probabilities)
        values = f_np_array(values)
        
        if (values is not None) and (probabilities.shape != values.shape):
            raise ValueError(' values and probabilities must have the same shape')
        if values is not None:
            # sort values : faster to look for x
            indices = np.argsort(values)
            values = values[indices]
            probabilities = probabilities[indices]        
        self.probabilities = probabilities
        self.values = values
        # a = indices, P = probability
        self.P,self.a = f_walker(self.probabilities) 
        cum = np.cumsum(self.probabilities)
        self.F_sum = cum[-1]
        self.cum = cum/self.F_sum
    def name():
        """Name of the class: 'Dist_walker'"""
        return 'Dist_walker'
    def rvs(self, size=1):
        """
        random numbers in ndarray of lenght size 
        
        Parameters
        ----------
        size : int 
            number of random number
        
        Returns
        -------
        ndarray
            random numbers         

        Examples
        --------
        >>> import qilum.stats as qs
        >>> walker = qs.Dist_walker([0.2, 0.5, 0.3], [0, 10, 2])
        >>> print('rans=',walker.rvs(10))
        rans= [ 0  0  0 10  0 10  2  2 10  0]
        """
        rans = np.random.uniform(0,1,size)    
        indices = np.zeros(size, dtype=np.int64)
        f_walker_ran(self.probabilities, self.P, self.a, size, rans, indices)
        if self.values is None:
            return indices        
        return self.values[indices]
    def f(self, x):
        """
        function f(x)
        
        Parameters
        ----------
        x : array_like of type(values) 
        
        Returns
        -------
        ndarray 
            f(x)
                     
        Examples
        --------
        >>> import qilum.stats as qs
        >>> walker = qs.Dist_walker([0.2, 0.5, 0.3], [0, 10, 2])
        >>> x = [0,1,2,3,4,5,6,7,8,9,10]
        >>> print('f(x)=',walker.f(x))
        f(x)= [0.2 0.  0.3 0.  0.  0.  0.  0.  0.  0.  0.5]
        """
        x = f_np_array(x)
        ys = np.zeros(x.size, dtype=self.probabilities.dtype)
        if self.values is None:
            xs_int = x.astype(int)
            indices = np.argwhere((xs_int-x==0) & (xs_int < self.probabilities.size) & (x >= 0))
            if indices.size > 0:
                ys[indices] = self.probabilities[xs_int[indices]] 
        else:
            # much less efficient
            for i in range(self.values.size):
                indices = np.argwhere(x==self.values[i])
                if indices.size > 0:
                    ys[indices] = self.probabilities[i]                                
        return ys
    def pmf(self, x):
        """Probability mass function
        
        Parameters
        ----------
        x : array_like of type(values) 
        
        Returns
        -------
        ndarray 
            f(x)/probabilities.sum()
        
        Examples
        --------
        >>> import qilum.stats as qs
        >>> walker = qs.Dist_walker([0.2, 0.5, 0.3], [0, 10, 2])
        >>> x = [0,1,2,3,4,5,6,7,8,9,10]
        >>> print('pmf(x)=',walker.pmf(x))
        pmf(x)= [0.2 0.  0.3 0.  0.  0.  0.  0.  0.  0.  0.5]
        """
        return self.f(x)/self.probabilities.sum()
    def pdf(self, x):
        """Same as pmf()"""
        return self.pmf(x)
    def cdf(self, x):
        """
        Cumulative distribution function.
        
        Parameters
        ----------
        x : array_like of type(values) 
        
        Returns
        -------
        ndarray 
           Cumulative distribution function evaluated at x 
        
        Examples
        --------
        >>> import qilum.stats as qs
        >>> walker = qs.Dist_walker([0.2, 0.5, 0.3], [0, 10, 2])
        >>> x = [0,1,2,3,4,5,6,7,8,9,10]
        >>> print('cdf(x)=',walker.cdf(x))
        cdf(x)= [0.2 0.2 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 1. ]
        """
        x = f_np_array(x)
        if self.values is None:
            indices = np.searchsorted(np.arange(0,self.probabilities.size), x, side='right')-1
            indices[indices==-1] = 0  # will not be used
            return np.where(x<0, 0, np.where(x>self.probabilities.size-1,1,self.cum[indices]))
        else:
            indices = np.searchsorted(self.values, x, side='right')-1
            indices[indices==-1] = 0  # will not be used
            return np.where(x<self.values[0], 0, np.where(x>self.values[-1],1,self.cum[indices]))
    def ppf(self, q):
        """
        Percent point function (inverse of cdf) at q 

        Parameters
        ----------
        q : array_like of double 
            lower tail probability
        
        Returns
        -------
        ndarray 
            quantile corresponding to the lower tail probability q
        
        Examples
        --------
        >>> import qilum.stats as qs
        >>> walker = qs.Dist_walker([0.2, 0.5, 0.3], [0, 10, 2])
        >>> q = [0,0.3,0.5,0.7,1]
        >>> print('ppf(q)=',walker.ppf(q))
        ppf(q)= [ 0.  2.  2. 10. 10.]        
        """
        q = f_np_array(q)
        indices = np.searchsorted(self.cum, q, side='left')
        if self.values is None:
            return np.where((q<0) | (q>1), np.NaN, indices)        
        else:
            return np.where((q<0) | (q>1), np.NaN, self.values[indices])        
    def F_tot():
        """Cumulative of the function f() on the whole valid range x
        
        Returns
        -------
        int 
           probabilities.sum()
        
        Examples
        --------
        >>> import qilum.stats as qs
        >>> walker = qs.Dist_walker([0.2, 0.5, 0.3], [0, 10, 2])
        >>> print(walker.F_tot())
        1.0   
        """
        return self.F_sum


# In[30]:


# distributions scale
class Dist_scale(Dist_qilum):
    """
    Distribution scale for x and y: f_new = scale_y*f((x-loc_x)*scale_x)
    
    Parameters
    ----------
    dist : scipy stats distribution or Dist_qilum
    loc_x : double
    scale_x : double 
        must be different of zero
    scale_y : double
        must be strictly positive 
    name : string 
        returned by :func:`name` 

    Examples
    --------
    >>> import qilum.stats as qs
    >>> import scipy.stats
    >>> # scipy dist
    >>> dist_exp = scipy.stats.expon()    
    >>> # scale scipy dist with negative scale_x and multiplicative factor scale_y
    >>> dist = qs.Dist_scale(dist_exp, loc_x=5, scale_x=-1, scale_y=2)
        
    .. image:: /_static/Dist_scale.jpg
        
    """
    def __init__(self, dist, loc_x=0, scale_x=1, scale_y=1, name=None):
        if scale_y < 0:
            raise ValueError('scale_y must be positive')
        if scale_x == 0:
            raise ValueError("scale_x can't be zero")
        self.dist = dist
        self.loc_x = loc_x
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.name_ = name
    def name(self):
        """Name of the class
        
        Returns
        -------
        string
            name if initialized;  dist.name() if exists; ortherwise 'Dist_scale'
        
        Examples
        --------
        >>> import qilum.stats as qs
        >>> import scipy.stats
        >>> dist = qs.Dist_scale(scipy.stats.expon(), loc_x=5, scale_x=-1, scale_y=2, name='Exp_scaled'))
        >>> dist.name()
        'Exp_scaled'        
        """
        if self.name_ is not None:
            return self.name_
        if hasattr(self.dist,'name'):
            if callable(getattr(self.dist, "name", None)):
                return self.dist.name()
        return 'Dist_scale'
    def rvs(self, size):
        """
        random numbers in ndarray of lenght size 
        
        Parameters
        ----------
        size : int 
            number of random number
        
        Returns
        -------
        ndarray
            random numbers         

        Examples
        --------
        >>> import qilum.stats as qs
        >>> import scipy.stats
        >>> dist = qs.Dist_scale(scipy.stats.expon(), loc_x=5, scale_x=-1, scale_y=2))
        >>> print('rans=',dist.rvs(4))
        rans= [4.19209864 3.58215396 4.37464038 3.62695892]
        """
        return self.scale_x*self.dist.rvs(size=size)+self.loc_x
    def rvs_xy(self, size):
        """
        random numbers rans in ndarray of lenght size and function(rans) 
        
        Parameters
        ----------
        size : int 
            number of random number
        
        Returns
        -------
        ndarray
            random numbers         
        ndarray
            f(random numbers)         

        Examples
        --------
        >>> import qilum.stats as qs
        >>> import scipy.stats
        >>> dist = qs.Dist_scale(scipy.stats.expon(), loc_x=5, scale_x=-1, scale_y=2))
        >>> print('rans=',dist.rvs_xy(2))
        rans= (array([4.58979217, 3.79870355]), array([1.32702468, 0.60160796]))
        """
        xs = self.rvs(size)
        return xs, self.f(xs)
    def f(self, x):
        """
        function f(x)
        
        Parameters
        ----------
        x : array_like of type(values) 
        
        Returns
        -------
        ndarray 
            f(x)
                     
        Examples
        --------
        >>> import qilum.stats as qs
        >>> import scipy.stats
        >>> dist = qs.Dist_scale(scipy.stats.expon(), loc_x=5, scale_x=-1, scale_y=2))
        >>> x = [0,1,2,3]
        >>> print('f(x)=',dist.f(x))
        f(x)= [0.01347589 0.03663128 0.09957414 0.27067057]
        """
        x = f_np_array(x)        
        return self.scale_y*self.dist.pdf((x-self.loc_x)/self.scale_x)
    def pdf(self, x):
        """Probability density function
        
        Parameters
        ----------
        x : array_like of type(values) 
        
        Returns
        -------
        ndarray 
            f(x)/F_tot()
        
        Examples
        --------
        >>> import qilum.stats as qs
        >>> import scipy.stats
        >>> dist = qs.Dist_scale(scipy.stats.expon(), loc_x=5, scale_x=-1, scale_y=2))
        >>> x = [0,1,2,3]
        >>> print('pdf(x)=',dist.pdf(x))
        pdf(x)= [0.00673795 0.01831564 0.04978707 0.13533528]
        """
        return self.f(x)/self.F_tot()
    def cdf(self, x ):
        """
        Cumulative distribution function.
        
        Parameters
        ----------
        x : array_like of type(values) 
        
        Returns
        -------
        ndarray 
           Cumulative distribution function evaluated at x 
        
        Examples
        --------
        >>> import qilum.stats as qs
        >>> import scipy.stats
        >>> dist = qs.Dist_scale(scipy.stats.expon(), loc_x=5, scale_x=-1, scale_y=2))
        >>> x = [0,1,2,3]
        >>> print('cdf(x)=',dist.cdf(x))
        cdf(x)= [0.00673795 0.01831564 0.04978707 0.13533528]
        """
        x = f_np_array(x)        
        y = self.dist.cdf((x-self.loc_x)/self.scale_x)
        if self.scale_x < 0:
            return 1.-y
        return y
    def ppf(self, q):
        """
        Percent point function (inverse of cdf) at q 

        Parameters
        ----------
        q : array_like of double 
            lower tail probability
        
        Returns
        -------
        ndarray 
            quantile corresponding to the lower tail probability q
        
        Examples
        --------
        >>> import qilum.stats as qs
        >>> import scipy.stats
        >>> dist = qs.Dist_scale(scipy.stats.expon(), loc_x=5, scale_x=-1, scale_y=2))
        >>> q = [0, 0.3,0.5,0.7,1]
        >>> print('ppf(q)=',dist.ppf(q))
        ppf(q)= [      -inf 3.7960272  4.30685282 4.64332506 5.        ]
        """
        q = f_np_array(q)
        if self.scale_x < 0:
            q = 1.-q
        x = self.dist.ppf(q)
        x = self.scale_x*x+self.loc_x
        return x
    def F_tot(self):
        """Cumulative of the function f() on the whole valid range x
        
        Returns
        -------
        int 
           dist.F_tot()*scale_y*|scale_x|; if F_tot() not define set to 1
        
        Examples
        --------
        >>> import qilum.stats as qs
        >>> import scipy.stats
        >>> dist = qs.Dist_scale(scipy.stats.expon(), loc_x=5, scale_x=-1, scale_y=2))
        >>> print(dist.F_tot())
        2   
        """
        tot = 1
        if hasattr(self.dist,'F_tot'):
            tot = self.dist.F_tot()
        return tot*self.scale_y*np.abs(self.scale_x)    


# In[15]:


# distribution of sum of distributions
class Dist_sum(Dist_qilum):
    """
    Distribution for a sum of distributions.
    
    Parameters
    ----------
    dists : array like
        array of scipy stats distributions or Dist_qilum

    Examples
    --------
    >>> import qilum.stats as qs
    >>> import scipy.stats
    >>> # exponential distributions left and right types
    >>> exp_left  = qs.Dist_scale(scipy.stats.expon(),loc_x=-1, scale_x=-1, scale_y=2, name='Exp+')
    >>> exp_right = qs.Dist_scale(scipy.stats.expon(),loc_x= 2, scale_x= 1, scale_y=3, name='Exp-')
    >>> dist = qs.Dist_sum([exp_left, exp_right]); 

    .. image:: /_static/Dist_sum.jpg
        
    """
    def __init__(self, dists):
        # transform in array of qilum_dist
        if not type(dists).__module__ == np.__name__:
            dists = np.array(dists)
        for i in range(dists.size):
            if not isinstance(dists[i], Dist_qilum):
                dists[i] = Dist_scale(dists[i])        
        self.dists = dists
        ys = np.zeros(self.dists.size, dtype = np.float64)
        for i in range(self.dists.size):
            ys[i] = self.dists[i].F_tot()
        self.walker = Dist_walker(ys)
    def name(self):
        """Name of the class
        
        Returns
        -------
        string
            'Dist_sum'
        
        Examples
        --------
        >>> import qilum.stats as qs
        >>> import scipy.stats
        >>> # exponential distributions left and right types
        >>> exp_left  = qs.Dist_scale(scipy.stats.expon(),loc_x=-1, scale_x=-1, scale_y=2, name='Exp+')
        >>> exp_right = qs.Dist_scale(scipy.stats.expon(),loc_x= 2, scale_x= 1, scale_y=3, name='Exp-')
        >>> dist = qs.Dist_sum([exp_left, exp_right]); 
        >>> dist.name()
        'Dist_sum'
        """
        return 'Dist_sum'
    def rvs(self, size):
        """
        random numbers in ndarray of lenght size 
        
        Parameters
        ----------
        size : int 
            number of random number
        
        Returns
        -------
        ndarray
            random numbers         

        Examples
        --------
        >>> import qilum.stats as qs
        >>> import scipy.stats
        >>> # exponential distributions left and right types
        >>> exp_left  = qs.Dist_scale(scipy.stats.expon(),loc_x=-1, scale_x=-1, scale_y=2, name='Exp+')
        >>> exp_right = qs.Dist_scale(scipy.stats.expon(),loc_x= 2, scale_x= 1, scale_y=3, name='Exp-')
        >>> dist = qs.Dist_sum([exp_left, exp_right]); 
        >>> print('rans=',dist.rvs(4))
        rans= [-1.69435547 -1.25739917 -1.01561614  4.38379953]
        """
        return self.rvs_xy(size)[0]
    def rvs_xy(self, size):
        """
        random numbers rans in ndarray of lenght size and function(rans) 
        
        Parameters
        ----------
        size : int 
            number of random number
        
        Returns
        -------
        ndarray
            random numbers         
        ndarray
            f(random numbers)         

        Examples
        --------
        >>> import qilum.stats as qs
        >>> import scipy.stats
        >>> # exponential distributions left and right types
        >>> exp_left  = qs.Dist_scale(scipy.stats.expon(),loc_x=-1, scale_x=-1, scale_y=2, name='Exp+')
        >>> exp_right = qs.Dist_scale(scipy.stats.expon(),loc_x= 2, scale_x= 1, scale_y=3, name='Exp-')
        >>> dist = qs.Dist_sum([exp_left, exp_right]); 
        >>> print('rans=',dist.rvs_xy(2))
        rans= (array([-1.90014397, -3.38554518]), array([0.81302226, 0.18407758]))
        """
        walker_indices_rans = self.walker.rvs(size)
        xs_rans = np.zeros(walker_indices_rans.size, dtype=np.float64)        
        ys_rans = np.zeros(walker_indices_rans.size, dtype=np.float64)        
        for i in range(self.dists.size):
            dist = self.dists[i]
            i_indices = np.where(walker_indices_rans == i)[0] 
            indices = walker_indices_rans[i_indices]
            xs,ys = dist.rvs_xy(i_indices.size)
            xs_rans[i_indices] = xs 
            ys_rans[i_indices] = ys
        return xs_rans, ys_rans
    def f(self, x):
        """
        function f(x)
        
        Parameters
        ----------
        x : array_like of type(values) 
        
        Returns
        -------
        ndarray 
            f(x)
                     
        Examples
        --------
        >>> import qilum.stats as qs
        >>> import scipy.stats
        >>> # exponential distributions left and right types
        >>> exp_left  = qs.Dist_scale(scipy.stats.expon(),loc_x=-1, scale_x=-1, scale_y=2, name='Exp+')
        >>> exp_right = qs.Dist_scale(scipy.stats.expon(),loc_x= 2, scale_x= 1, scale_y=3, name='Exp-')
        >>> dist = qs.Dist_sum([exp_left, exp_right]); 
        >>> x = [-3,1,2,3]
        >>> print('f(x)=',dist.f(x))
        f(x)= [0.27067057 0.         3.         1.10363832]
        """
        x = f_np_array(x)        
        y = np.zeros(x.size, dtype = np.float64)
        for i in range(self.dists.size):
            y += self.dists[i].f(x)
        return y
    def pdf(self, x):
        """Probability density function
        
        Parameters
        ----------
        x : array_like of type(values) 
        
        Returns
        -------
        ndarray 
            f(x)/F_tot()
        
        Examples
        --------
        >>> import qilum.stats as qs
        >>> import scipy.stats
        >>> # exponential distributions left and right types
        >>> exp_left  = qs.Dist_scale(scipy.stats.expon(),loc_x=-1, scale_x=-1, scale_y=2, name='Exp+')
        >>> exp_right = qs.Dist_scale(scipy.stats.expon(),loc_x= 2, scale_x= 1, scale_y=3, name='Exp-')
        >>> dist = qs.Dist_sum([exp_left, exp_right]); 
        >>> x = [-3,1,2,3]
        >>> print('pdf(x)=',dist.pdf(x))
        pdf(x)= [0.05413411 0.         0.6        0.22072766]
        """
        x = f_np_array(x)        
        return self.f(x)/self.F_tot()
    def cdf(self, x ):
        """
        Cumulative distribution function.
        
        Parameters
        ----------
        x : array_like of type(values) 
        
        Returns
        -------
        ndarray 
           Cumulative distribution function evaluated at x 
        
        Examples
        --------
        >>> import qilum.stats as qs
        >>> import scipy.stats
        >>> # exponential distributions left and right types
        >>> exp_left  = qs.Dist_scale(scipy.stats.expon(),loc_x=-1, scale_x=-1, scale_y=2, name='Exp+')
        >>> exp_right = qs.Dist_scale(scipy.stats.expon(),loc_x= 2, scale_x= 1, scale_y=3, name='Exp-')
        >>> dist = qs.Dist_sum([exp_left, exp_right]); 
        >>> x = [-3,1,2,3]
        >>> print('cdf(x)=',dist.cdf(x))
        cdf(x)= [0.05413411 0.4        0.4        0.77927234]
        """
        x = f_np_array(x)        
        y = np.zeros(x.size, dtype = np.float64)
        for i in range(self.dists.size):
            y += self.dists[i].cdf(x)*self.dists[i].F_tot()
        return y/self.F_tot()
    def ppf(self, q):
        """
        Percent point function (inverse of cdf) at q 

        Parameters
        ----------
        q : array_like of double 
            lower tail probability
        
        Returns
        -------
        ndarray 
            quantile corresponding to the lower tail probability q
        
        Examples
        --------
        >>> import qilum.stats as qs
        >>> import scipy.stats
        >>> # exponential distributions left and right types
        >>> exp_left  = qs.Dist_scale(scipy.stats.expon(),loc_x=-1, scale_x=-1, scale_y=2, name='Exp+')
        >>> exp_right = qs.Dist_scale(scipy.stats.expon(),loc_x= 2, scale_x= 1, scale_y=3, name='Exp-')
        >>> dist = qs.Dist_sum([exp_left, exp_right]); 
        >>> q = [0, 0.3,0.5,0.7,1]
        >>> print('ppf(q)=',dist.ppf(q))
        NotImplementedError: Sum::ppf: not implemented
        """
        q = f_np_array(q)
        raise NotImplementedError('Sum::ppf: not implemented')
    def F_tot(self):
        """Cumulative of the function f() on the whole valid range x
        
        Returns
        -------
        int 
           dist.F_tot()*scale_y*|scale_x|; if dist.F_tot() not define set to 1
        
        Examples
        --------
        >>> import qilum.stats as qs
        >>> import scipy.stats
        >>> # exponential distributions left and right types
        >>> exp_left  = qs.Dist_scale(scipy.stats.expon(),loc_x=-1, scale_x=-1, scale_y=2, name='Exp+')
        >>> exp_right = qs.Dist_scale(scipy.stats.expon(),loc_x= 2, scale_x= 1, scale_y=3, name='Exp-')
        >>> dist = qs.Dist_sum([exp_left, exp_right]); 
        >>> print(dist.F_tot())
        5   
        """
        tot = 0
        for i in range(self.dists.size):
            tot += self.dists[i].F_tot()
        return tot


# In[16]:


# distributions rejection

class Dist_reject(Dist_qilum):
    """
    Distribution with rejection method. Give a distribution with a known method for both random number generation and function value, and apply rejection method to keep values
    
    Parameters
    ----------
    dist_ran : distribution scipy or qilum.Dist 
        we can call a random number generator :func:`rvs`
    f_fx : function 
        objective
    f_tot : double
        Cumulative of the function f_fx() on the whole valid range x, 
        Only used if we want to use this distribution as part of Dist_sum 

    Examples
    --------
    >>> import qilum.stats as qs
    >>> import scipy.stats
    >>> # gaussian function
    >>> def f_f(xs):
    ...     return 3.*np.exp(-np.square(xs)/10.)
    >>>
    >>> # 1.create a function f_sum(x) above the function f_f(x).
    >>> #   f_sum(x) = y0*exp(+a*x)  if x_min < x 
    >>> #   f_sum(x) = step function if x_min < x <= x_max 
    >>> #   f_sum(x) = y0*exp(-a*x)  if x_max < x               
    >>> xs = np.linspace(-5,5, 1001)
    >>> ys = f_f(xs)    
    >>> xs_inter, ys_inter = qs.f_max(xs, ys, 6)    
    >>> ys_inter *= 1.2 # just to be sure that our step function >= f_f() 
    >>> # histogram distribution with the step function
    >>> hist_dist = scipy.stats.rv_histogram((ys_inter, xs_inter))
    >>> # scale this diribution
    >>> cumulative = ((np.roll(xs_inter,-1)-xs_inter)[:-1]*ys_inter).sum()
    >>> step = qs.Dist_scale(hist_dist, scale_y = cumulative)
    >>> 
    >>> # exponential distribution at the left and right of the step distribution
    >>> exp_left  = qs.Dist_scale(scipy.stats.expon(),loc_x=xs_inter[-1], scale_x=1, scale_y=ys_inter[-1], name='Exp+')
    >>> exp_right = qs.Dist_scale(scipy.stats.expon(),loc_x=xs_inter[0]-1e-10, scale_x=-1,scale_y=ys_inter[0], name='Exp-')
    >>> 
    >>> # 2. create a sum of the known distributions for each part of f2 function
    >>> dist_sum    = qs.Dist_sum([exp_left, step, exp_right]) 
    >>> # 3. create the Dist_rejection distribution using this sum and the original f_f(x) function        
    >>> dist = qs.Dist_reject(dist_sum, f_f)
    >>> 
    >>> # test result with the normal distribution hypothesis
    >>> k2, p = scipy.stats.normaltest(dist.rvs(100000))
    >>> print("Normal distribution test = ",p > 1e-3, " with ", "p = {:g}".format(p))        
    Normal distribution test =  True  with  p = 0.0617403
    
    .. image:: /_static/Dist_reject.jpg
        
    """    
    def __init__(self, dist_ran, f_fx, f_tot = None):
        if not isinstance(dist_ran, Dist_qilum):
            dist_ran = Dist_scale(dist_ran)        
        self.dist_ran = dist_ran
        self.f_fx = f_fx
        self.success = 0
        self.f_tot = f_tot
    def name(self):
        """Name of the class
        
        Returns
        -------
        string
            'Dist_reject'
        
        Examples
        --------
        >>> # see example at the top of the class
        >>> dist.name()
        'Dist_reject'
        """
        return 'Dist_reject'
    def rvs(self, size):
        """
        random numbers in ndarray of lenght size 
        
        Parameters
        ----------
        size : int 
            number of random number
        
        Returns
        -------
        ndarray
            random numbers         

        Examples
        --------
        >>> # see example at the top of the class
        >>> print('rans=',dist.rvs(4))
        rans= [-1.17789338 -0.69306554  1.1672123  -1.80663854]
        """
        needed_rans = size
        xs_res = np.zeros(needed_rans, dtype=float)
        i_start = 0
        success_all = 0
        N_all = 0
        while needed_rans>0:
            needed_rans = int(needed_rans)
            xs_rans, ys_rans = self.dist_ran.rvs_xy(int(size*1.1))
            ys = self.f_fx(xs_rans)
                               
            # dist_Accept ran
            indices_neg = np.argwhere(ys_rans < ys)
            if indices_neg.size>0:
                indice = indices_neg[0]
                err = ''
                err += 'ys_rans < ys: indices.size= {}/{}'.format(indices_neg.size, ys_rans.size)
                err += ', [0]: (i,x,y,y_under)={},{},{},{}'.format(indice,xs_rans[indice],ys[indice],ys_rans[indice])                                                                         
                raise Exception(err)
            indices = np.argwhere(ys/ys_rans > np.random.uniform(0.,1.,ys_rans.size))[:,0] 
 
            i_end = min(indices.size,xs_res.size-i_start)
            success = min(indices.size/needed_rans,1)
            success_all += indices.size
            N_all += xs_rans.size
            # print('i_start, i_end, success=',i_start,i_end, success)
            xs_res[i_start:i_start+i_end] = (xs_rans[indices])[:i_end]
            i_start += i_end
            needed_rans = int((xs_res.size - i_start)/min(1,max(success, 0.5)))                                                     
        self.success = success_all/N_all
        return xs_res
    def rvs_xy(self, size):
        """
        random numbers rans in ndarray of lenght size and function(rans) 
        
        Parameters
        ----------
        size : int 
            number of random number
        
        Returns
        -------
        ndarray
            random numbers         
        ndarray
            f(random numbers)         

        Examples
        --------
        >>> # see example at the top of the class
        >>> print('rans=',dist.rvs_xy(2))
        rans= (array([-2.46439985, -0.96670812]), array([1.63441612, 2.73234395]))
        """
        x = self.rvs(size)
        return x, self.f(x)
    def f(self, x):
        """
        function f(x) set initialy f_fx(x)
        
        Parameters
        ----------
        x : array_like of type(values) 
        
        Returns
        -------
        ndarray 
            f(x)
                     
        Examples
        --------
        >>> # see example at the top of the class
        >>> x = [-3,1,2,3]
        >>> print('f(x)=',dist.f(x))
        f(x)= [1.21970898 2.71451225 2.01096014 1.21970898]
        """
        x = f_np_array(x)        
        return self.f_fx(x)
    def pdf(self, x):
        """Probability density function
        
        Parameters
        ----------
        x : array_like of type(values) 
        
        Returns
        -------
        ndarray 
            f(x)/F_tot()
        
        Examples
        --------
        >>> # see example at the top of the class
        >>> x = [-3,1,2,3]
        >>> print('pdf(x)=',dist.pdf(x))
        NotImplementedError: Dist_reject.F_tot: not implemented        
        """
        x = f_np_array(x)        
        return self.f(x)/self.F_tot()
    def f_underlying(self, x):
        """
        function dist_ran.f(x): function of the underlying distribution dist_ran set up initialy 
        
        Parameters
        ----------
        x : array_like of type(values) 
        
        Returns
        -------
        ndarray 
            dist.f(x)
                     
        Examples
        --------
        >>> # see example at the top of the class
        >>> x = [-3,1,2,3]
        >>> print('f_underlying(x)=',dist.f_underlying(x))
        f_underlying(x)= [2.7056004  3.6        2.75102576 2.75102576]
        >>> # or similarly
        >>> print('f_underlying(x)=',dist.dist_ran.f(x))
        f_underlying(x)= [2.7056004  3.6        2.75102576 2.75102576]
        """
        return self.dist_ran.f(x)
    def cdf(self, x ):
        """
        Cumulative distribution function.
        
        Parameters
        ----------
        x : array_like of type(values) 
        
        Returns
        -------
        ndarray 
           Cumulative distribution function evaluated at x 
        
        Examples
        --------
        >>> # see example at the top of the class
        >>> x = [-3,1,2,3]
        >>> print('cdf(x)=',dist.cdf(x))
        NotImplementedError: Dist_reject.cdf: not implemented
        """
        x = f_np_array(x)        
        raise NotImplementedError('Dist_reject.cdf: not implemented')
    def ppf(self, q):
        """
        Percent point function (inverse of cdf) at q 

        Parameters
        ----------
        q : array_like of double 
            lower tail probability
        
        Returns
        -------
        ndarray 
            quantile corresponding to the lower tail probability q
        
        Examples
        --------
        >>> # see example at the top of the class
        >>> q = [0, 0.3,0.5,0.7,1]
        >>> print('ppf(q)=',dist.ppf(q))
        NotImplementedError: Dist_reject.ppf: not implemented
        """
        q = f_np_array(q)
        raise NotImplementedError('Dist_reject.ppf: not implemented')
    def F_tot(self):
        """Cumulative of the function f() on the whole valid range x
        
        Returns
        -------
        int 
           
        
        Examples
        --------
        >>> # see example at the top of the class
        >>> print(dist.F_tot())
        NotImplementedError: Dist_reject.F_tot: not implemented   
        """
        if self.f_tot is not None:
            return self.f_tot
        raise NotImplementedError('Dist_reject.F_tot: not implemented')    


# In[17]:


# Distribution cubic spline

def f_cs_help(xs, ys, N=1000):
    if (np.roll(xs,-1)<= xs)[:-1].sum() > 0:
        raise ValueError(' `x` must be strictly increasing sequence')
    if (ys<0).sum() > 0:
        raise ValueError(' `y` must be positive')    
    if N > xs.size:
        f_cs = scipy.interpolate.CubicSpline(xs, ys) 
        xs = np.linspace(xs[0], xs[-1], N)
        ys = f_cs(xs)        
    # cumulative
    cum = f_cumulative(xs, ys)
    F_sum = cum[-1] 
    cum /= cum[-1]
    # remove the 0s and 1s at the beginning and the end
    indices = np.where(cum <=0)[0]
    start = 0
    if indices.size>0: 
        start = indices[-1]  
    indices = np.where(cum >=1)[0]
    end = indices[0]+1
    cum2 = cum[start:end]
    xs2 = xs[start:end]
    return F_sum, scipy.interpolate.CubicSpline(cum2, xs2), scipy.interpolate.CubicSpline(xs2, cum2) 

class Dist_cubicSpline(Dist_qilum):
    """
    Distribution for (x,y): cubic splaine approximation for both cumulative ans values
    
    Parameters
    ----------
    x : array like 
    y : array like 
    N_cs : int
        number of point to set up the cubic spline

    Examples
    --------
    >>> import qilum.stats as qs
    >>> # test function: truncated gaussian
    >>> def f_f(xs):
    ...     return 3.*np.exp(-np.square(xs)/10.)
    >>> 
    >>> # initialize class
    >>> x = np.linspace(-12, 12, 51)
    >>> y = f_f(x)  
    >>> dist = qs.Dist_cubicSpline(x, y, N_cs=1000)
    
    .. image:: /_static/Dist_cubicSpline.jpg
        
    """    
    def __init__(self, x, y, N_cs=1000):
        x = f_np_array(x)        
        y = f_np_array(y)        
        self.xs = x
        self.ys = y
        self.f_cs = scipy.interpolate.CubicSpline(x, y) 
        self.scale, self.F_cs, self.Fx_cs = f_cs_help(x, y, N_cs)         
    def name(self):
        """Name of the class
        
        Returns
        -------
        string
            'Dist_reject'
        
        Examples
        --------
        >>> x = np.linspace(-12, 12, 51)
        >>> dist = qs.Dist_cubicSpline(x, y= 3.*np.exp(-np.square(x)/10.), N_cs=1000)
        >>> dist.name()
        'Dist_cubicSpline'
        """
        return 'Dist_cubicSpline'
    def rvs(self, size):
        """
        random numbers in ndarray of lenght size 
        
        Parameters
        ----------
        size : int 
            number of random number
        
        Returns
        -------
        ndarray
            random numbers         

        Examples
        --------
        >>> x = np.linspace(-12, 12, 51)
        >>> dist = qs.Dist_cubicSpline(x, y= 3.*np.exp(-np.square(x)/10.), N_cs=1000)
        >>> print('rans=',dist.rvs(4))
        rans= [ 3.1874446  -0.24592411 -2.9817858  -1.65194734]
        """
        ran = np.random.uniform(0,1,size)
        return self.F_cs(ran)        
    def rvs_xy(self, size):
        """
        random numbers rans in ndarray of lenght size and function(rans) 
        
        Parameters
        ----------
        size : int 
            number of random number
        
        Returns
        -------
        ndarray
            random numbers         
        ndarray
            f(random numbers)         

        Examples
        --------
        >>> x = np.linspace(-12, 12, 51)
        >>> dist = qs.Dist_cubicSpline(x, y= 3.*np.exp(-np.square(x)/10.), N_cs=1000)
        >>> print('rans=',dist.rvs_xy(2))
        rans= (array([-0.17748735,  1.35683644]), array([2.9905203 , 2.49554626]))
        """
        x = self.rvs(size)
        y = self.f(x)
        return x,y         
    def f(self, x):
        """
        Cubic spline of (x,y)
        Approximation: should be 1/F'(F_inverse(x)), but very small error 
        
        Parameters
        ----------
        x : array_like of type(values) 
        
        Returns
        -------
        ndarray 
            f(x)
                     
        Examples
        --------
        >>> x = np.linspace(-12, 12, 51)
        >>> dist = qs.Dist_cubicSpline(x, y= 3.*np.exp(-np.square(x)/10.), N_cs=1000)
        >>> x = [-3,1,2,3]
        >>> print('f(x)=',dist.f(x))
        f(x)= [1.21972729 2.71451285 2.01096922 1.21972729]
        """
        x = f_np_array(x)        
        return np.where((x<self.xs[0]) | (x>self.xs[-1]) , 0, self.f_cs(x))  
    def pdf(self, x):
        """
        Probability density function.
        Cubic spline of (x,y)
        
        Parameters
        ----------
        x : array_like of type(values) 
        
        Returns
        -------
        ndarray 
            f(x)/F_tot()
        
        Examples
        --------
        >>> x = np.linspace(-12, 12, 51)
        >>> dist = qs.Dist_cubicSpline(x, y= 3.*np.exp(-np.square(x)/10.), N_cs=1000)
        >>> x = [-3,1,2,3]
        >>> print('pdf(x)=',dist.pdf(x))
        pdf(x)= [0.07253817 0.16143427 0.11959396 0.07253817]
        """
        x = f_np_array(x)        
        return np.where((x<self.xs[0]) | (x>self.xs[-1]) , 0, self.f_cs(x)/self.scale)  
    def cdf(self, x):
        """
        Cumulative distribution function.
        
        Parameters
        ----------
        x : array_like of type(values) 
        
        Returns
        -------
        ndarray 
           Cumulative distribution function evaluated at x 
        
        Examples
        --------
        >>> x = np.linspace(-12, 12, 51)
        >>> dist = qs.Dist_cubicSpline(x, y= 3.*np.exp(-np.square(x)/10.), N_cs=1000)
        >>> x = [-3,1,2,3]
        >>> print('cdf(x)=',dist.cdf(x))
        cdf(x)= [0.09161441 0.67650553 0.81730869 0.91187099]
        """
        x = f_np_array(x)        
        y = np.where((x<self.Fx_cs.x[0]), 0, np.where((x>self.Fx_cs.x[-1]) , 1, self.Fx_cs(x)))  
        y[y>1] = 1
        y[y<0] = 0
        return y
    def ppf(self, q):
        """
        Percent point function (inverse of cdf) at q 

        Parameters
        ----------
        q : array_like of double 
            lower tail probability
        
        Returns
        -------
        ndarray 
            quantile corresponding to the lower tail probability q
        
        Examples
        --------
        >>> x = np.linspace(-12, 12, 51)
        >>> dist = qs.Dist_cubicSpline(x, y= 3.*np.exp(-np.square(x)/10.), N_cs=1000)
        >>> q = [0, 0.3,0.5,0.7,1]
        >>> print('ppf(q)=',dist.ppf(q))
        ppf(q)= [-12.          -1.19663998  -0.02402402   1.14859193  11.97597598]
        """
        q = f_np_array(q)
        x = np.where(q<0, np.NaN, np.where(q>1 , np.NaN, self.F_cs(q)))  
        x[x<self.Fx_cs.x[0]] = self.Fx_cs.x[0]
        x[x>self.Fx_cs.x[-1]] = self.Fx_cs.x[-1]
        return x
    def F_tot(self):
        """Cumulative of the function f() on the whole valid range x
        
        Returns
        -------
        int 
           
        
        Examples
        --------
        >>> x = np.linspace(-12, 12, 51)
        >>> dist = qs.Dist_cubicSpline(x, y= 3.*np.exp(-np.square(x)/10.), N_cs=1000)
        >>> print(dist.F_tot())
        16.81497238763992   
        """
        return self.scale


# In[ ]:




