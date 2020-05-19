from __future__ import print_function
import numpy as np
import matplotlib
try:
    import matplotlib.pyplot as plt
except:
    print("cannot import matplotlib")
import timeit
import scipy.stats as st
import os


def plot_single(spect,soapout=None,fmin=None,fmax=None,tsft=None,tstart=None):


    if tstart is None:
        tstart = None

    if fmin is None and fmax is None:
        fmin = 0
        fmax = len(spect[0])

    if tsft is None:
        tsft = (fmax-fmin)/len(spect[0])

    nsft = len(soapout.vit_track)
    tick_fontsize = 13
    label_fontsize = 20

    fig, ax = plt.subplots(nrows=2,figsize=(18,11),sharex=True)
    xticks = np.linspace(0,(nsft-1)*tsft,10)
    yticklabels = np.round(np.linspace(fmin,fmax,8),2).astype(int)
    yticks = np.linspace(0,len(spect[0]),8).astype(int)
    plot_spect = np.ma.masked_where(spect == 96., spect,copy = True)
    
    im = ax[0].imshow(plot_spect.T,cmap="YlGnBu",aspect="auto",origin="lower")
    imv = ax[1].imshow(soapout.vitmap.T,cmap="YlGnBu",aspect="auto",origin="lower")
    cbar = fig.colorbar(im,ax = ax[0])
    cbarv = fig.colorbar(imv,ax = ax[1])
    cbar.set_label("Normalised SFT power",fontsize = label_fontsize)
    cbarv.set_label("log-viterbi 'probability'",fontsize = label_fontsize)
    cbar.ax.tick_params(labelsize=tick_fontsize)
    cbarv.ax.tick_params(labelsize=tick_fontsize)
    line = ax[0].scatter(np.arange(nsft),soapout.vit_track,color="red",label="Viterbi track",s=3)
    ax[0].set_xticks((xticks)/(tsft))
    ax[1].set_xticks((xticks)/(tsft))
    ax[0].set_yticks(yticks)
    ax[1].set_yticks(yticks)
    ax[0].set_xticklabels(xticks)
    ax[0].set_yticklabels(yticklabels)
    ax[1].set_xticklabels(xticks)
    ax[1].set_yticklabels(yticklabels)

    ax[1].set_xlabel("Time - {}[s]".format(tstart),fontsize=label_fontsize)
    ax[0].set_ylabel("Frequency [Hz]",fontsize=label_fontsize)
    ax[1].set_ylabel("Frequency [Hz]",fontsize=label_fontsize)
    ax[1].xaxis.set_tick_params(rotation=0,labelsize=tick_fontsize)
    ax[0].yaxis.set_tick_params(rotation=0,labelsize=tick_fontsize)
    ax[1].yaxis.set_tick_params(rotation=0,labelsize=tick_fontsize)
    ax[0].set_xlim([0,nsft])
    ax[1].set_xlim([0,nsft])
    ax[0].set_ylim([0,len(spect[0])])
    ax[1].set_ylim([0,len(spect[0])])

    for spine in list(ax[0].spines.values()) + list(ax[1].spines.values()):
        spine.set_visible(False)
        
    cbar.outline.set_visible(False)
    cbarv.outline.set_visible(False)
    fig.subplots_adjust(wspace=0, hspace=0)
    return fig, (im,imv,line)
