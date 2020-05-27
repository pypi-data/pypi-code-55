# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 11:00:46 2020

@author: jcnossen1
"""

from photonpy.cpp.context import Context
import numpy as np
import matplotlib.pyplot as plt
import photonpy.cpp.multi_emitter as multi_emitter
from photonpy.cpp.gaussian import Gaussian, Gauss3D_Calibration
from photonpy.cpp.simflux import SIMFLUX
import photonpy.cpp.com as com

useSimflux = True

# Simflux modulation patterns
mod = np.array([
     [0, 1.8, 0, 0.95, 0, 1/6],
     [1.9, 0, 0, 0.95, 0, 1/6],
     [0, 1.8, 0, 0.95, 2*np.pi/3, 1/6],
     [1.9, 0, 0, 0.95, 2*np.pi/3, 1/6],
     [0, 1.8, 0, 0.95, 4*np.pi/3, 1/6],
     [1.9, 0, 0, 0.95, 4*np.pi/3, 1/6]
])



def generate_positions(N,E,K,roisize,bg):
    """
    Generate a parameter vector with either 2D or 3D layout:
    2D: background, X0, Y0, I0, X1, Y1, I1, ....
    3D: background, X0, Y0, Z0, I0, X1, Y1, Z1, I1, ....
    
    N: Number of ROIs
    E: Number of emitters per ROI
    K: Number of parameters per emitter (3 for 2D or 4 for 3D)
    """
    pts = np.zeros((N,E*K+1))
    pts[:,0] = bg #bg
    border = 4
    for k in range(E):
        if K==3: # 2D case
            pos = np.random.uniform([border,border,1000],[roisize-1-border,roisize-1-border,2000],size=(N,K))
        if K==4: # 3D case
            pos = np.random.uniform([border,border,0,400],[roisize-border-1,roisize-border-1,0,600],size=(N,K))

        pts[:,np.arange(K)+k*K+1] = pos

    return pts

def result_to_str(result):
    K = 3
    E = len(result)//K
    xpos = result[1::K]
    ypos = result[2::K]
    I = result[3::K]  # in 3D it would be 4::K
        
    prev = np.get_printoptions()['precision']
    np.set_printoptions(precision=1)
    s = f"{E} emitters: I={I}, X={xpos}, Y={ypos}"
    np.set_printoptions(precision=prev)
    return s

    

with Context(debugMode=True) as ctx:
    sigma = 1.8
    roisize = 20
    E = 2
    N = 1
    pixelsize=0.1
    
    psf = Gaussian(ctx).CreatePSF_XYIBg(roisize, sigma, True)
    sf = SIMFLUX(ctx).CreateEstimator_Gauss2D(sigma, mod, roisize, len(mod), True)
    K = psf.NumParams()-1

    bg = 10
    if useSimflux:     #simflux?
        psf = sf
        bg /= len(mod) # in simflux convention, background photons are spread over all frames
    
    border = 3
    minParam = [border, border, 200, 2]
    maxParam = [roisize-1-border,roisize-1-border, 4000, 20]

    # Create a list of estimator objects, one for each number of emitters
    max_emitters = E
    estimators = [multi_emitter.CreateEstimator(psf, k, ctx, minParam, maxParam) for k in range(1+max_emitters)]
    for e in estimators:
        e.SetLevMarParams(1e-16, 50)
        
    true_pos = generate_positions(N, E, K, roisize, bg)
    smp = estimators[E].GenerateSample(true_pos)
    
    if useSimflux:
        plt.figure()
        plt.imshow(np.concatenate(smp[0],-1))
    
    com_estim = com.CreateEstimator(roisize,ctx)
        
    results=estimators[E].Estimate(smp, initial=true_pos)[0]
    current_ev = estimators[E].ExpectedValue(results)

    emittercount = np.ones(N,dtype=np.int32)
    for roi in range(N): # go through all ROIs
    
        roi_smp = smp[roi]
        

        # First state is only background
        current = [np.mean(roi_smp)]
        current_ev = np.ones(psf.sampleshape) * current[0]
        
        numEmitters = 0

        for c in np.arange(1, max_emitters+1):
            residual = np.maximum(0, roi_smp - current_ev)
                        
            residual_com = psf.Estimate([residual])[0][0]
            
            current = [*current, residual_com[0], residual_com[1], residual_com[2]]

            print(f"Initial estimate for {c} emitters: {residual_com}")
            current = np.array(current)
            
            results, _, traces = estimators[c].Estimate([roi_smp], initial=[current])
            results = results[0]

            print(results)
            current_ev = estimators[c].ExpectedValue([results])[0]            

            current = results
            numEmitters += 1

