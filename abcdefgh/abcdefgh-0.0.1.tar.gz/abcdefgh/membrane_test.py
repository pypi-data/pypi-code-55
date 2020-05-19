import numpy as np

from scipy.optimize import curve_fit

def expfunc(x, a, b, c):
    return a * np.exp(-b * x) + c

def expfuncinv(x, a, b, c):
    return a * (1 - np.exp(-b * x)) + c

def membrane_test(sig, cmd, sf, fit_region = (0.8, 0.1), whole_cell = True, positive_peak=True):
    
    """
    The membrane test protocol must be such that the command pulse occupies the first half of each sweep.
    
    The calculation are performed as follows:
    1) The input resistance Rinput is derived from the input voltage step and output command step: Rinput = Vstep / Istep 
    2) The membrane time constant tau is derived from an exponential fit to the capacitive transient
    3) The charge of the membrane Q is calculated by integrating the capacitive transient
    4) The access resistance is derived as Ra = tau * Vstep / Q
    5) The membrane resistance is derived as Rm = Rinput - Ra
    6) The membrane capacitance is derived as Cm tau * Rinput / (Ra * Rm)
    7) The holding current is the current at baseline level
    
    Parameters : 
    
        - sig : numpy array - Output signal in units of pA.
        - cmd : numpy array - Input signal in units of mV.
        - sf : float - Sampling frequency of the signal in units of Hz.
        - fit_region : tuple of float -  Default is (0.8, 0.1).
        - whole_cell : boolean - If False, only Rinput and the holding level are calculated (in bath and seal configuration). Default is True.
        - positive_peak : boolean - If True, the calculation is performed based on the upward capacitive transient. If False, on the downward capacitive transient. Default is True.
        
    Returns :
    
        - Rinput : float - Input resistance in units of MOhm.
        - Ra : float - Access resistance in units of MOhm.
        - Rm : float - Membrane resistance in units of MOhm.
        - Cm : float - Membrane capacitance in units of pF.
        - tau : float - Membrane time constant in units of µs.
        - holding : float - Holding current in units of pA. 
    
    Example :
    
    Rinput, Ra, Rm, Cm, tau, holding = membrane_test(sig, cmd, sf, fit_region = (0.8, 0.1), whole_cell = True, positive_peak = True)
    
    See also : expfunc, expfuncinv, scipy.optimize.curve_fit
    
    """

    Rinput, Ra, Rm, Cm, tau, holding = None, None, None, None, None, None
    
    # time array
    t = np.arange(0.0, sig.size/sf, 1/sf) # s
    
    # number of samples used to fit the capacitive transient to an exponential (eg 1/3 of a sweep)
    nsamples_fit = int(t.size / 3)
    # number of samples used to calculate the baseline levels (eg 20 % of a voltage pulse, ie 20 % of half a sweep)
    nsamples_baseline = int(0.2 * t.size / 2)

    # voltage level at steady-state
    V_baseline1, V_baseline2 = np.mean(cmd[-nsamples_baseline:]), np.mean(cmd[int(t.size / 2) - nsamples_baseline:int(t.size / 2)])
    # current level at steady-state
    I_baseline1, I_baseline2 = np.mean(sig[-nsamples_baseline:]), np.mean(sig[int(t.size / 2) - nsamples_baseline:int(t.size / 2)])
    
    #holding = (I_baseline1 + I_baseline2) / 2 # pA
    holding = I_baseline1
    
    Istep = I_baseline2 - I_baseline1 # pA
    Vstep = V_baseline2 - V_baseline1 # mV

    Rinput = Vstep / Istep * pow(10,3) # MOhm
        
    if whole_cell == True:
        
        # Positive peak
        
        if positive_peak == True:

            #imax = np.where(sig == np.max(sig[:nsamples_fit]))[0][0]
            imax = np.argmax(sig[:nsamples_fit])
            peak = sig[imax] - I_baseline2 # pA
            start = imax + np.where(sig[imax:] - I_baseline2 < fit_region[0] * peak)[0][0]
            stop = imax + np.where(sig[imax:] - I_baseline2 < fit_region[1] * peak)[0][0]

            (param1, param2, param3), cov = curve_fit(expfunc, t[start:stop] - t[start], sig[start:stop] - I_baseline2)
            tau = pow(10,6)/param2 # ms

            Q = np.sum(sig[imax:imax + nsamples_fit] - expfuncinv(t[0:nsamples_fit], I_baseline2 - I_baseline1, param2, I_baseline1)) / sf # pC

        # Negative peak
        
        else:

            #imax = np.where(sig == np.min(sig[nsamples_fit:]))[0][0]
            imax = nsamples_fit + np.argmin(sig[nsamples_fit])
            peak = sig[imax] - I_baseline1 # pA
            start = imax + np.where(sig[imax:] - I_baseline1 > fit_region[0] * peak)[0][0]
            stop = imax + np.where(sig[imax:] - I_baseline1 > fit_region[1] * peak)[0][0]

            (param1, param2, param3), cov = curve_fit(expfunc, t[start:stop] - t[start], abs(sig[start:stop] - I_baseline1))
            tau = pow(10,6)/param2 # µs

            Q = np.sum(- sig[imax:imax + nsamples_fit] + expfunc(t[0:nsamples_fit], I_baseline2 - I_baseline1, param2, I_baseline1)) / sf # pC

        Ra = tau * Vstep / Q * pow(10, -3) # MOhm

        Rm = Rinput - Ra # MOhm

        Cm = tau * Rinput / (Ra * Rm) # pF

        Rinput, Ra, Rm, Cm, tau, holding = np.around(Rinput), np.around(Ra), np.around(Rm), np.around(Cm), np.around(tau), np.around(holding)
        
    else :
        
        Rinput, holding = np.around(Rinput, 1), np.around(holding)
    
    return Rinput, Ra, Rm, Cm, tau, holding