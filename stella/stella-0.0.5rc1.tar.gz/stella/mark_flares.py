import numpy as np
from tqdm import tqdm
import more_itertools as mit
from astropy import units as u
from astropy.table import Table
from scipy.signal import medfilt
from scipy.signal import find_peaks
from scipy.optimize import minimize
from scipy.interpolate import interp1d

from .utils import *

__all__ = ['FitFlares']


class FitFlares(object):
    """
    Uses the predictions from the neural network
    and identifies flaring events based on consecutive
    points. Users define a given probability threshold
    for accpeting a flare event as real.
    """

    def __init__(self, id, time, flux, flux_err, predictions):
        """
        Uses the times, fluxes, and predictions defined
        in stella.ConvNN to identify and fit flares, as
        well as do injection-recovery for completeness.
        
        Parameters
        ----------
        time : np.array
             Array of times to find flares on.
        flux : np.array
             Array of light curves.
        flux_err : np.array
             Array of errors on light curves.
        predictions : np.array
             Array of predictions for each light curve
             passed in.
        
        Attributes
        ----------
        ids : np.array
        time : np.ndarray
        flux : np.ndarray
        flux_err : np.ndarray
        predictions : np.ndarray
        """
        self.IDs        = id
        self.time       = time
        self.flux       = flux
        self.flux_err   = flux_err
        self.predictions = predictions


    def group_inds(self, values):
        """
        Groups regions marked as flares (> prob_threshold) for
        flare fitting. Indices within 4 of each other are grouped
        as one flare.

        Returns
        -------
        results: np.ndarray
             An array of arrays, which are groups of indices
             supposedly attributed with a single flare.
        """
        results = []

        for i, v in enumerate(values):
            if i == 0:
                mini = maxi = v
                temp = [v]
            else:
                # SETS 4 CADENCE LIMIT
                if (np.abs(v-maxi) <= 3):
                    temp.append(v)
                    if v > maxi:
                        maxi = v
                    if v < mini:
                        mini = v
                else:
                    results.append(temp)
                    mini = maxi = v
                    temp = [v]
                
                # GETS THE LAST GROUP
                if i == len(values)-1:
                    results.append(temp)

        return np.array(results)


    def get_init_guesses(self, groupings, time, flux, err, prob, 
                         maskregion, region):
        """
        Guesses at the initial t0 and amplitude based on 
        probability groups.

        Parameters
        ----------
        groupings : np.ndarray
             Group of indices for a single flare event.
        time : np.array
        flux : np.array
        err : np.array
        prob : np.array

        Returns
        -------
        tpeaks : np.ndarray
             Array of tpeaks for each flare group.
        amps : np.ndarray
             Array of amplitudes at each tpeak.
        """
        tpeaks = np.array([])
        ampls  = np.array([])

        if len(groupings) > 0:
            for g in groupings:
                gmin, gmax = g[0], g[-1]
                
                if gmin-maskregion < 0:
                    subreg = np.arange(0, gmax+maskregion, 1, dtype=int)
                elif gmax+maskregion > len(time):
                    subreg = np.arange(len(time)-maskregion, len(time), 1, dtype=int)
                else:
                    subreg = np.arange(gmin-maskregion, gmax+maskregion, 1, dtype=int)

                # LOOKS AT REGION AROUND FLARE                                                                 
                subt = time[subreg]
                subf = flux[subreg]
                sube = err[subreg]
                subp = prob[subreg]
                
                doubcheck = np.where(subp>=self.threshold)[0]
            
                # FINDS HIGHEST "PROBABILITY" IN FLARE                                                         
                if len(doubcheck) > 1:
                    peak = np.argmax(subf[doubcheck])
                    t0   = subt[doubcheck[peak]]
                    amp  = subf[doubcheck[peak]]
                    
                else:
                    t0  = subt[doubcheck]
                    amp = subf[doubcheck]

                tpeaks  = np.append(tpeaks, t0)
                ampls   = np.append(ampls,  amp)

        return tpeaks, ampls


    def identify_flare_peaks(self, threshold=0.5):
        """
        Finds where the predicted value is above the threshold
        as a flare candidate. Groups consecutive indices as one
        flaring event.
        
        Parameters
        ----------
        threshold : float, optional
             The probability threshold for believing an event
             is a flare. Default is 0.5.

        Attributes
        ----------
        treshold : float
        flare_table : astropy.table.Table
             A table of flare times, amplitudes, and equivalent
             durations. Equivalent duration given in units of days.
        """
        self.threshold = threshold

        def chiSquare(var, x, y, yerr, t0_ind):
            """ Chi-square fit for flare parameters. """
            amp, rise, decay = var
            m, p = flare_lightcurve(x, t0_ind, amp, rise, decay)
            return np.sum( (y-m)**2.0 / yerr**2.0 )
            

        table = Table(names=['Target_ID', 'tpeak', 'amp', 'dur',
                             'rise', 'fall', 'prob'])
        kernel_size = 15

        for i in tqdm(range(len(self.IDs)), desc='Finding & Fitting Flares'):
            time = self.time[i]
            flux = self.flux[i]
            err  = self.flux_err[i]
            prob = self.predictions[i]
            
            where_prob_higher = np.where(prob >= threshold)[0]
            groupings = self.group_inds(where_prob_higher)

            tpeaks, amps = self.get_init_guesses(groupings, time, flux,
                                                 err, prob, 2, 50)

            # FITS PARAMETERS TO FLARE
            for tp, amp in zip(tpeaks,amps):
                # CASES FOR HANDLING BIG FLARES
                if amp > 1.3:
                    region = 400
                    maskregion = 150
                else:
                    region = 40
                    maskregion = 10

                where = np.where(time >= tp)[0][0]
                
                subt = time[where-region:where+region]
                subf = flux[where-region:where+region]
                sube = err[ where-region:where+region]
                subp = prob[where-region:where+region]
                amp_ind = int(len(subf)/2)

                mask = np.zeros(len(subt))
                mask[int(amp_ind-maskregion/2.):int(amp_ind+maskregion)] = 1
                m = mask == 0

                if len(mask) > 10:
                    func = interp1d(subt[m], medfilt(subf[m], kernel_size=kernel_size))

                    # REMOVES LOCAL STELLAR VARIABILITY TO FIT FLARE
                    try:
                        detrended = subf/func(subt) 
                        std = np.nanstd(detrended[m])
                        med = np.nanmedian(detrended[m])
                    except:
                        pass

                    # MARKS FLARE AMPLITUDE AND POINTS BEFORE & AFTER
                    amp1 = detrended[amp_ind]# - med
                    decay  = subf[amp_ind+2]
                    growth = subf[amp_ind-2]
                
                    if amp > 1.5:
                        decay_guess = 0.008
                        rise_guess  = 0.003
                    else:
                        decay_guess = 0.001
                        rise_guess  = 0.0001
                        
                    if ( (amp1 > (med+1.5*std) )):
                        if  (detrended[amp_ind+1] >= med+1.0*std) and (decay <= amp):
                            if (growth < amp) and ((amp-subf[amp_ind+1]) < 2):
                                amp1 -= med
                                
                                x = minimize(chiSquare, x0=[amp1, rise_guess, decay_guess],
                                             bounds=((amp1-0.1,amp1+0.1), (0.0001,0.01),
                                                     (0.001, 0.01)),
                                             args=(subt, detrended, sube, amp_ind),
                                             method='L-BFGS-B')

                                if x.x[0] > 1.5 or (x.x[0]<1.5 and x.x[2]<0.4):
                                    fm, params = flare_lightcurve(subt, amp_ind, np.nanmedian([amp1, x.x[0]]),
                                                                  x.x[1], x.x[2])
                                    
                                    params[1] = x.x[0]#subf[amp_ind]
                                    params[2] = (params[2] * u.min).value / 2
                                    params = np.append(params, subp[amp_ind])
                                    params = np.append(np.array([self.IDs[i]]), params)
                                    table.add_row(params)

        self.flare_table = table
