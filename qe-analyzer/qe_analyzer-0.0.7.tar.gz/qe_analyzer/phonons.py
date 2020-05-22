import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as spc

def importFreqGp(fname):
    """
    imports data from *.freq.gp file

    Parameters
    ----------
    fname : str
        DESCRIPTION.file name to be imported

    Returns
    -------
    x: 1-d numpy array
        DESCRIPTION. k point x-value for plotting (2pi/a)
    energy: 2-d numpy array
        DESCRIPTION. each column is a different band.

    """
    #frequencies originally listed in cm^-1 
    arr=[]
    #conv=spc.h*spc.c/spc.elementary_charge*100*1000
    with open(fname, "r") as f:
        for line in f.readlines():
            lineStr=line.split()
            arr.append(lineStr)
    a=np.array(arr, np.float)
    [r,c]=a.shape
    x=a[:,0]
    energy=a[:,1:c]
    return x, energy

def generateXcoordMatdyn(matdynFile):
    """
    generates X-labels (special K-points) from matdyn file
    assumes q_in_band_form=True

    Parameters
    ----------
    matdynFile : TYPE
        DESCRIPTION.

    Returns
    -------
    pts : 2-d numpy array
        DESCRIPTION. special points such that column 0 is kx, column 1 is ky, column 2 is kz, column 3 is the x-coordinate for the E-vs-k plot
    flfrq : str
        DESCRIPTION. filename from matdyn file for where to expect the phonon data for processing (*.freq.gp file)

    """

    
    pts=[]
    flfrq=''
    with open(matdynFile, "r") as f:
        lines=f.readlines()
        cnt=0
        
        while lines[cnt][0] != "/" :
            L=lines[cnt].strip().split()
            if L[0]=='flfrq':
                potential=L[2].replace(',', '')
                potential=potential.replace('\'', '')
                flfrq=potential+".gp"
            cnt=cnt+1
        numpts=int(lines[cnt+1])
        x=0.0
        kprev=[0.0, 0.0, 0.0]
        pnts=np.zeros((numpts, 4))
        for k in range(numpts):
            L=lines[cnt+2+k].split()
            L=np.array(L, float)
            if k==0:
                x=0.0
                kprev=L
            else:
                kMag=np.sqrt((L[0]-kprev[0])**2+(L[1]-kprev[1])**2+(L[2]-kprev[2])**2)
                kprev=L
                x=x+kMag
        
            pnts[k, 0]=L[0]
            pnts[k,1]=L[1]
            pnts[k,2]=L[2]
            pnts[k,3]=x
        pts=pnts
    return pts, flfrq
    
            
    

def plotPhononDispersion_cm(matdynF, figsize=plt.rcParams.get('figure.figsize'), pad=1.08 ,labels=[]):
    """
    Plots phonon dispersion assuming q_in_band_form for special points
    
    plotPhononDispersion_cm('diamond_matdyn.in')
    plotPhononDispersion_cm('diamond_matdyn.in', labels=['L', r'$\Gamma$', 'X'])

    Parameters
    ----------
    matdynF : str
        DESCRIPTION. Filename of the matdyne input file that you used to generate the *.freq.gp file
    figsize : tuple, optional
        DESCRIPTION. The default is plt.rcParams.get('figure.figsize'). See matplotlib.pyplot.plot for details
    pad : float, optional
        DESCRIPTION. The default is 1.08. padding around the figure in plt.tight_layout()
    labels : list of strings, optional
        DESCRIPTION. The default is []. Labels to use for the special points. 
        If the length of this is not equal to the number of special points listed in matdynF, these labels will not be used.
        assumes q_in_band_form

    Returns
    -------
    None.

    """

    #find frequency
    specPts, fname=generateXcoordMatdyn(matdynF)
    [x, energy]=importFreqGp(fname)
    
    plt.figure(figsize=plt.rcParams.get('figure.figsize'))
    plt.ylabel(r'Frequency ($cm^{-1}$)')
    [r,c]=energy.shape
    for kp in range(c):
        plt.plot(x, energy[:, kp], color='C0')
    plt.gca().set_ylim(bottom=0)
    plt.xlabel('k-point path')
    plt.xlim((min(x), max(x)))
    row, col=specPts.shape
    
    
    if len(labels)==row:
        plt.xticks(ticks=specPts[:, 3], labels=labels)
    else:
        plt.xticks(ticks=specPts[:, 3], labels=specPts[:,0:3])
        
        
        
    plt.tight_layout(pad=pad)
    plt.show()
def plotPhononDispersion_meV(matdynF, figsize=plt.rcParams.get('figure.figsize'), pad=1.08 ,labels=[]):
    """
    Plots phonon dispersion assuming q_in_band_form for special points
    
    plotPhononDispersion_meV('diamond_matdyn.in')
    plotPhononDispersion_meV('diamond_matdyn.in', labels=['L', r'$\Gamma$', 'X'])
    

    Parameters
    ----------
    matdynF : str
        DESCRIPTION. Filename of the matdyne input file that you used to generate the *.freq.gp file
    figsize : tuple, optional
        DESCRIPTION. The default is plt.rcParams.get('figure.figsize'). See matplotlib.pyplot.plot for details
    pad : float, optional
        DESCRIPTION. The default is 1.08. padding around the figure in plt.tight_layout()
    labels : list of strings, optional
        DESCRIPTION. The default is []. Labels to use for the special points. 
        If the length of this is not equal to the number of special points listed in matdynF, these labels will not be used.
        assumes q_in_band_form

    Returns
    -------
    None.

    """

    #find frequency
    specPts, fname=generateXcoordMatdyn(matdynF)
    conv=spc.h*spc.c/spc.elementary_charge*100*1000
    [x, energy]=importFreqGp(fname)
    
    plt.figure(figsize=plt.rcParams.get('figure.figsize'))
    plt.ylabel(r'Energy (meV)')
    [r,c]=energy.shape
    for kp in range(c):
        plt.plot(x, energy[:, kp]*conv, color='C0')
    plt.gca().set_ylim(bottom=0)
    plt.xlabel('k-point path')
    plt.xlim((min(x), max(x)))
    row, col=specPts.shape
    
    
    if len(labels)==row:
        plt.xticks(ticks=specPts[:, 3], labels=labels)
    else:
        plt.xticks(ticks=specPts[:, 3], labels=specPts[:,0:3])
        
        
        
    plt.tight_layout(pad=pad)
    plt.show()    