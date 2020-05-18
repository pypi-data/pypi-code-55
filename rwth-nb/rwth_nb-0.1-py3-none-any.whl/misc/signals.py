"""
This module defines functionality related to signal processing.
"""

import numpy as np
from scipy.signal import find_peaks # peak finder

# t axis in seconds
(t, deltat) = np.linspace(-10, 10, 5001, retstep=True)  

# Elementary signals
gauss     = lambda t: np.exp(-(t)**2)
unitstep  = lambda t: np.where(t>=0, 1, 0)
rect      = lambda t: unitstep(t+0.5) - unitstep(t-0.5)
tri       = lambda t: rect(t/2)*(1-abs(t))
si        = lambda t: np.sinc(t/np.pi) # English notation sinc(t) = sin(pi t)/(pi t)
rc_tp     = lambda f: 1 / (1 + 1j * 2 * np.pi * f) # RC = 1
rl_hp     = lambda f: (1j * 2 * np.pi * f) / (1 + 1j * 2 * np.pi * f) # RL = 1

eps = np.finfo(float).eps # floating point accuracy



def dft(s, fs, NFFT=0):
    """
    Calculate discrete Fourier transform of vector s
    Sampling frequency fs is used to calculate frequency vector f
    Number of frequency coefficients can be specified as well
    """
    if NFFT==0: 
        NFFT = len(s) # int(2**np.ceil(np.log2(len(bla))))
    
    S = np.fft.fftshift(np.fft.fft(s, NFFT))/NFFT
    f = np.linspace(-fs/2,fs/2, NFFT)
    
    return S, f


def idft(S, Ntime=0, NFFT=0):
    """
    Calculate discrete inverse Fourier transform of vector S
    Number of time bins is used to crop the output of NumPy's ifft function
    Number of frequency coefficients can be specified as well
    """
    if NFFT == 0: NFFT = len(S)
    
    s = np.fft.ifft(np.fft.ifftshift(S*NFFT), NFFT)
    
    if not Ntime == 0:
        s = s[0:Ntime]
    
    return s


def find_intervals(s, t, thresh, delta):
    """
    Find intervals of signal s by searching for delta-functions in the second derivative of s

    Parameters
    ----------
    s : array_like
        The signal
        
    t : array_like
        Corresponding t-axis
        
    thresh : float
        Threshold for delta search
        
    delta : float
        Sampling period

    Returns
    -------
    intervals_s, peaks, dd : *intervals* are the intervals, *peaks* the found peaks and *dd* the second derivative of s.
    """
        
    # derivative of derivative shows delta functions at discontinuities
    dd = np.diff(np.diff(s, prepend=0), prepend=0)/delta**2 
    
    # find delta functions
    peaks, _  = find_peaks(np.abs(dd), prominence=thresh) 
    
    # return interval limits in seconds
    intervals = np.round(t[peaks]*10)/10
    
    return intervals, peaks, dd


def find_ind_least_diff(x, x0):
    """
    Find index of the value that's nearest to x0

    Parameters
    ----------
    x : array_like
        Array to be inspected

    x0 : float
        Target value to be searched for

    Returns
    -------
    index : int or list
        index(indices) of value(s) that is (are) nearest to x0
    """
    
    if isinstance(x0, list) or isinstance(x0, np.ndarray):
        return list(map(lambda t0: np.abs(x - t0).argmin(), x0))
    else:
        return np.abs(x - x0).argmin()

