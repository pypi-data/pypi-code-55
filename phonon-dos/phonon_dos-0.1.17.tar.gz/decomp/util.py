#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:33:25 2019

@author: gc4217
"""
from scipy.optimize import curve_fit
import numpy as np
import os

def repeat_masses(Masses, n_atom_conventional_cell, n_atom_primitive_cell, N1, N2, N3):
    repeated_masses = np.array([])
    repeated_masses_for_ani = np.array([])
    for i in range(len(Masses)):
        mass = Masses[i]

        n = n_atom_conventional_cell[i]
        nprim = n_atom_primitive_cell[i]
        
        m = np.repeat(mass, N1*N2*N3*3*n)
        m_ani = np.repeat(mass,nprim*3)
        
        repeated_masses = np.concatenate((repeated_masses,m))
        repeated_masses_for_ani = np.concatenate((repeated_masses_for_ani,m_ani))
        
    masses = np.array(repeated_masses).flatten()
    masses_for_animation = np.array(repeated_masses_for_ani).flatten()
    
    return masses, masses_for_animation

def corr(tall,X,Y,tau,mode):
    M = len(tall)
    dt = tall[1] - tall[0]
    tmax = M - tau
    N = np.size(X[0]) 
    X0 = X[0:tmax,:]
    X2 = 1/tmax*np.sum(X[0:tmax,:]*X[0:tmax,:])
    C = []
    for n in range(tau):
        print(n)
        Xjj = Y[n:n+tmax,:]
        a = np.multiply(np.conjugate(X0),Xjj)
        b = 1/(tmax) * np.sum(a,axis=0)#/X2
        if (mode=='projected'):
            c = b
        else:
            c = np.sum(b)
        C.append(c)
    C = np.array(C)
    t = np.arange(0,tau)*dt
    freq = np.fft.fftfreq(tau,d=dt)
    Z = np.fft.fft(C,axis=0)
    return t, C, freq, Z

def lorentzian(x, x0, A, gamma):
    y = 1/np.pi *  A * 1/2*gamma / ((x - x0)**2 + (1/2*gamma)**2)
    return y

def save(filename, data):
    filename2 = filename
    if os.path.isfile(filename):
        n_of_files = len([name for name in os.listdir('.') if (os.path.isfile(name) and name==filename)])
        filename2 = filename+'_'+str(n_of_files)
        print(filename, ' already present. Saving it as ', filename2)
    np.savetxt(filename2,data) 
    return

def save_append(filename, data1, data2):
    filename2 = filename
#    if os.path.isfile(filename):
#        n_of_files = len([name for name in os.listdir('.') if (os.path.isfile(name) and name==filename)])
#        filename2 = filename+'_'+str(n_of_files)
#        print(filename, ' already present. Saving it as ', filename2)
        
    file = open(filename2,'ab')
    np.savetxt(file,data1)
    np.savetxt(file,data2)
    file.close()
    return

def max_freq(dt_ps, tau):
    #you want the max frequency plotted be 25 Thz
    max_freq = 0.5*1/dt_ps
    if (max_freq < 25):
        meta = int(tau/2)
    else:
        meta = int(tau/2*25/max_freq)
    return meta

def fit_to_lorentzian(x_data, y_data, k, n):
    try:
        if(n in [0,1,2] and np.allclose(k, [0,0,0])): #if acoustic modes at Gamma, don't fit anything
                popt, pcov = np.zeros(3), np.zeros((3,3))
        else:
            popt, pcov = curve_fit(lorentzian, x_data, y_data)
    except RuntimeError:
        print('\t\tWasnt able to fit to Lorentzian mode '+str(n)+'\n\n')
        x0 = x_data[np.argwhere(y_data==y_data.max())]
        y0 = y_data.max()
        popt, pcov = np.array([x0,y0,0]), np.zeros((3,3))
    perr = np.sqrt(np.diag(pcov))
    return popt, perr

def create_Tkt(Num_timesteps, tot_atoms_uc, N1N2N3, Vt, R0, k):
    N = tot_atoms_uc*N1N2N3
    Vcoll = np.zeros((Num_timesteps,tot_atoms_uc*3),dtype=complex)  
    for j,h,l in zip(range(tot_atoms_uc*3),np.repeat(range(0,N),3)*N1N2N3*3,np.tile(range(0,3),tot_atoms_uc)):
        vels = np.array(Vt[:,h+l:h+N1N2N3*3:3],dtype=complex)
        poss = R0[h:h+N1N2N3*3:3,:]
        x = np.multiply(vels,np.exp(-1j*np.dot(poss,k)))
        Vcoll[:,j] = np.sum(x,axis=1)
    Tkt = Vcoll  
    return Tkt


def pair_distr(file_initial_conf, Rt, Nsteps, dr):
    N = len(Rt[0,0::3])
    ang_to_bohr = 1.8897259886
    SCell = np.genfromtxt(file_initial_conf, skip_header=2, max_rows=3)*ang_to_bohr
    A1, A2, A3 = SCell[0,:], SCell[1,:], SCell[2,:]
    V = np.dot(A1, np.cross(A2, A3))
    L = V**(1/3)
#    dr = .01 #[B] 
    r = np.arange(0,L/2,dr)
    Nbins = len(r)-1
    
    HIST = np.zeros(Nbins)
    for t in range(Nsteps):
        print(t)
        hist = np.zeros(Nbins)
        Rx, Ry, Rz = Rt[t,0::3], Rt[t,1::3], Rt[t,2::3]
#        vtx, vty, vtz = Vt[t,0::3],  Vt[t,1::3], Vt[t,2::3]
    #    R0x, R0y, R0z = R0[::3,0], R0[::3,1], R0[::3,2]
    
        Rmatx, Rmaty, Rmatz = np.tile(Rx,(N,1)).T, np.tile(Ry,(N,1)).T, np.tile(Rz,(N,1)).T
        Rijx, Rijy, Rijz = Rmatx - Rx, Rmaty - Ry, Rmatz - Rz
    
    
        for i in range(N):
    #        vi = np.sqrt(vtx[i]**2+vty[i]**2+vtz[i]**2)
            for j in range(N):
    #            vj = np.sqrt(vtx[j]**2+vty[j]**2+vtz[j]**2) 
                if(i==j):
                    continue
                rijx, rijy, rijz = Rijx[i,j], Rijy[i,j], Rijz[i,j]
                rij = np.sqrt(rijx**2+rijy**2+rijz**2)
                BIN = int(rij/dr) 
                if (BIN < Nbins):
                    hist[BIN] = hist[BIN] + 3 #3*vi*vj 
        HIST = HIST + hist
                        
    const = 4/3 * np.pi* N/V  
    g = np.zeros(Nbins)
    for b in range(Nbins):
        rlower = b*dr
        rupper = (b+1)*dr
        nid = const*(rupper**3-rlower**3)
        g[b] = HIST[b]/N/Nsteps/nid
        
    return r[0:-1], g
