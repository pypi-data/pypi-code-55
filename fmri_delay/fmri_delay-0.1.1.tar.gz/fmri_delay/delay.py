#!/usr/bin/env python
# coding: utf-8

import numpy as np
from multiprocessing import Pool
from itertools import combinations, permutations
from scipy import stats, sparse
from tqdm import tqdm
import time

import istarmap

def delay_per_timepoint(vox, activ, t, delay_list, n_regions):
    '''
    Delay measurement routine for a particular timepoint:
    '''

    # Initializing delay measures as a sparse matrix for each "active" time point
    #delay_meas = sparse.lil_matrix((n_regions, n_regions), dtype = float)
    delay_meas = sparse.lil_matrix((n_regions, n_regions), dtype = np.uint16)
    # Store index of previously (act) and newly (vox) activated regions 
    act_idx = np.where(activ != 0)[0]
    vox_idx = np.where(vox != 0)[0]
    
    # Computation of time delay between
    if any(activ):
        for vox_id in vox_idx:
            delay_meas[act_idx, vox_id] = (t + 1 - activ[act_idx])
    
    delay_list.append(delay_meas)
    
    # Update activation list and times
    activ[np.where(vox != 0)] = t + 1
    
    return

def par_delay(vox_1, vox_2):
    '''
    Parallel implementation of Delay Measurement Algorithm:
    '''
    
    timepoints, activ = np.where(np.array([vox_1, vox_2]).T != 0)
    
    n_act = len(activ)
    
    my_del = np.full((2, n_act - 1), np.nan)
    
    simul = False
    prev_act = np.full((2), np.nan)
    
    for i in range(0, n_act, 1):
        
        my_del[1 - activ[i], i - 1] = timepoints[i] - prev_act[1 - activ[i]]
        
        if simul:
            prev_act[activ[i - 1]] = timepoints[i - 1]
            
        simul = ((i + 1 < n_act) and (timepoints[i] == timepoints[i + 1]))
        
        if not simul:
            prev_act[activ[i]] = timepoints[i]
    
    results = np.empty((2, 2))
    for i, row in enumerate(my_del):
        no_nan = row[~np.isnan(row)]
        if len(no_nan) > 1:
            results[:, i] = no_nan.mean(), no_nan.std()
        else:
            print('Warning: only one delay encountered!')
            results[:, i] = no_nan.mean(), np.nan
    
    return results

def delay_measure(signal, return_meas = False, pre_thresh = None, parallel = True, progress = False, v = False, **kwargs):
    '''
    Main delay framework algorithm:
    '''
    #reload(logging)
    #logging.basicConfig(filename = 'delay_perf.log', level = logging.INFO, filemode = 'w')
    
    n_regions = len(signal)
    n_timepoints = len(signal[0])

    if v:
        print('Working with {} regions and {} timepoints'.format(n_regions, n_timepoints))

    delay_mean = np.full((n_regions, n_regions), np.nan)
    delay_std = np.full_like(delay_mean, np.nan)

    tb_meas = time.perf_counter()
    
    if parallel:
        if v:
            print('Using Parallel Implementaion')

        indices = np.transpose(np.triu_indices_from(delay_mean, 1))

        if v:
            print('Measuring delays...')
        #logging.info('Measuring delays...')

        if pre_thresh is not None:
            if v:
                print('Pre-thresholding of innovation signals...')
            signal_t = signal.copy()
            signal_t[abs(stats.zscore(signal_t, axis = None)) < pre_thresh] = 0
        else:
            signal_t = signal

        n_tasks = sum(1 for _ in combinations(signal_t, 2))
        #delay_measures = []

        if progress:
            prog_func = tqdm
        else:
            prog_func = lambda x: x

        with Pool(processes = None) as pool:
            for idx, pool_res in enumerate(prog_func(pool.istarmap(par_delay, combinations(signal_t, 2), **kwargs))):
                    for i, perm in enumerate(permutations(indices[idx])):
                        delay_mean[perm] = pool_res[0][i]
                        delay_std[perm] = pool_res[1][i]

                ## Old methods
                #delay_measures = pool.starmap(par_delay, combinations(signal, 2), **kwargs)
                #delay_measures = list(pool.istarmap(par_delay, combinations(signal, 2), **kwargs))

            ta_meas = time.perf_counter()
            if v:
                print('Measurement done after {}s.'.format(ta_meas - tb_meas))
            #logging.info('Measure done in {}s.'.format(ta_meas - tb_meas))

    else:
        if v:
            print('Using Straight Forward Implementaion')
        # Initialization of data vectors
        activ = np.zeros((n_regions))
        delay_list = []
        
        if v:
            print('Measuring delays...')
        #logging.info('Measuring delays...')
        
        # Scanning through time
        for t, vox in enumerate(signal.T):
            
            # Progression Verbose
            #if ((t+1) % np.ceil(n_timepoints/10) == 0):
            #    print('––', t+1, 'out of', n_timepoints)
            
            # Compute delay and update activation list iif at least one region is active
            if any(vox):
                delay_per_timepoint(vox, activ, t, delay_list, n_regions)
        
        ta_meas = time.perf_counter()
        if v:
            print('Measurement done after {}s.'.format(ta_meas - tb_meas))
        #logging.info('Measure done in {}s.'.format(ta_meas - tb_meas))
        
        n_active = len(delay_list)
        
        if v:
            print('Computing mean and STD ({} out of {} time points)...'.format(n_active, n_timepoints))
        #logging.info('Computing mean and STD ({} out of {} time points)...'.format(n_active, n_timepoints))
        
        for row_id in range(n_regions):
            tmp = np.empty((n_regions, n_active))
            
            for t in range(n_active):
                tmp[:, t] = delay_list[t].getrow(row_id).toarray()
                
            tmp[tmp == 0] = np.nan
            
            delay_mean[row_id] = np.nanmean(tmp, axis = 1)
            delay_std[row_id] = np.nanstd(tmp, axis = 1)

            delay_mean[row_id, row_id] = np.nan
            delay_std[row_id, row_id] = np.nan
        
        ta_comp = time.perf_counter()
        if v:
            print('Computation done after {}s.'.format(ta_comp - ta_meas))
        #logging.info('Computation done in {}s.'.format(ta_comp - ta_meas))
    #print('–#– Delay Measurement Succeeded –#–')
    #logging.info('–#– Delay Measurement Succeeded –#–')
    
    if return_meas:
        return delay_list, delay_mean, delay_std
    else:
        return delay_mean, delay_std