import glob
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import scipy.constants as spc
def extractECUTConvergenceInfo(file1):
	"""extracts ECUT convergence information from a given file, file1
	outputs a list of [ECUT, # planewaves, energy, CPU time, and ECUT**(3/2)]
	
	Parameters
    ----------
    file1 : str
        DESCRIPTION. File to read in
	
    Returns list containing
    -------
    ecutwfc : float
        DESCRIPTION. ECUT value 
	planewaves : float
        DESCRIPTION. number of planewaves
	energy : float
        DESCRIPTION. Total Energy
	ecutwfc**(3/2): float
		DESCRIPTION. ECUT value to the 2/3 power. Ecut**(2/3) should be proportional to the number of planewaves
	
	"""
    
	d=open(file1, 'r')

	lines=d.readlines()
	d.close()
	energy=0.0
	time=0.0
	planewaves=0
	ecutwfc=0.0
	for k in range(len(lines)):
			#pull out ecut
		Line=lines[k].strip()
		if len(Line)>4:
			if Line[0:4]=='iter':
				Lparse=Line.split()
				ecutwfc=float(Lparse[4])
			#pull out energy
			if Line[0]=='!':
				Lparse=Line.split()
				energy=float(Lparse[4])
				time=s+60*mn+60*60*hr
			#pull out number planewaves
			if Line[0:3]=="Sum":
				Lparse=Line.split()
				planewaves=int(Lparse[-1])
	return [ecutwfc, planewaves, energy, ecutwfc**(3/2)]

def ECUTconvergenceTest(head, calcThresh=False, thresh=0.05):
	""" Prints the filenames imported  for an ECUT convergence test (series of files where ECUT is changing)
	assumes '${head}${ECUT}.out' file naming, 
	will ignore all other files in folder.
	Prints the filenames that it imports for this also saves the plot
    

    Parameters
    ----------
    head : str
        DESCRIPTION. The header to the filename. Assumes that your working directory contains files with 
		   '${head}${ECUT}.out' formatting
	calcThresh : boolean, optional
		DESCRIPTION. Do you want to pull out the ECUT associated with a convergence threshold?
	
	thresh : float
		DESCRIPTION. The convergence threshold you would like
	delim : str
		DESCRIPTION. delimiter right before listing of ECUT
    Returns
    -------
    None. A plot should show up and will be automatically saved to your working directory.
    """
	dall=[]    
	g="./"+head+"*.out"
	#g='./'+head+"*.out"
	print(glob.glob(g))
	for filepath in glob.iglob(g):
		d=extractECUTConvergenceInfo(filepath)
		dall.append(d)
	#energies in Ry
	df=pd.DataFrame(dall, columns=['ecutwfc', 'planewaves', 'energy', 'ecutwfc3halves'])
	dfinal=df.sort_values('ecutwfc')
	intF=interp1d(dfinal['ecutwfc'], dfinal['energy'], kind='linear')

	mn=min(dfinal['energy'])
	x=np.linspace(min(dfinal['ecutwfc']), max(dfinal['ecutwfc']), 100)
	toEv=spc.physical_constants['Rydberg constant times hc in eV'][0]
	f=plt.figure(1)
	plt.plot(x, intF(x)*toEv-mn*toEv, '--',dfinal['ecutwfc'], dfinal['energy']*toEv-mn*toEv, 'o')
	plt.xlabel('ECUT (Ry)')
	plt.ylabel('Total energy (eV)-minimum Energy' )
	plt.title(head + " ECUT convergence")
	plt.ylim(0,max(dfinal['energy']*toEv-mn*toEv))
	plt.tight_layout()
	plt.savefig(head+'_ECUTconvergencePlot')
	plt.show()

	if calcThresh:
		Es=min(dfinal['energy'])*toEv-mn*toEv+1E-12
		Estart=np.log10(Es)
		Ee=max(dfinal['energy'])*toEv-mn*toEv
		Eend=np.log10(Ee)

		y=np.logspace(Estart, Eend, 100)
		intFInv=interp1d((dfinal['energy']-mn)*toEv, dfinal['ecutwfc'],kind='linear', bounds_error=False)
		x=intFInv(y)
		plt.plot(intFInv(y), y, color='C4')

		plt.show()
		print(intFInv(thresh))
def extractKConvergenceInfo(file1):
    """
    kx, ky, kz, shiftx, shifty, shiftx, ecutwfc, energy, inequiv,time  =extractKConvergenceInfo('SrTiO3-260-0-16.out')

    Parameters
    ----------
    file1 : str
        DESCRIPTION. name of *.out file to extract information from

    Returns
    -------
    kx : int
        DESCRIPTION.# k points in x direction
    ky : int
        DESCRIPTION. # k points in y direction
    kz : int
        DESCRIPTION. # k points in z direction
    shiftx : int
        DESCRIPTION.0 or 1
    shifty : int
        DESCRIPTION.0 or 1
    shiftz : int
        DESCRIPTION.0 or 1
    ecutwfc : float
        DESCRIPTION. cutoff energy
    energy : float
        DESCRIPTION. total energy
    inequiv : int
        DESCRIPTION. Number inequivalent k points
    time : float
        DESCRIPTION. CPU time in minutes

    """
    #time in minutes
    #gets kx, ky, kz and shifts from *.in file (assumes only one decimal point before *.out)
    energy=0.0
    kx=0
    ky=0
    kz=0
    shiftx=0
    shifty=0
    shiftz=0
    inequiv=0
    time=0.0
    planewaves=0
    ecutwfc=0.0
    
    idx=file1.rfind('.')
    fIn=file1[0:idx]+'.in'
    with open(fIn, "r") as f:
        read=False
        for line in f.readlines():

            if read==True:
                L=line.strip().split()
                kx=int(L[0])
                ky=int(L[1])
                kz=int(L[2])
                shiftx=int(L[3])
                shifty=int(L[4])
                shiftz=int(L[5])
                read=False
            if 'K_POINTS'==line[0:8]:
                read=True
    with open(file1, 'r') as f:
        for line in f.readlines():
            L=line.strip()
            if len(L)>12:
                
                if L[0:4]=='iter':
                    Lparse=L.split()
                    ecutwfc=float(Lparse[4])

                #pull out energy
                if L[0]=='!':
                    Lparse=L.split()
                    energy=float(Lparse[4])
                #pull out time
                if L[0:2]=='PW':
                    Lparse=L.split()[2][0:-1]
                    Lparse1=Lparse.split('h')
                    
                    Lparse2=Lparse1[len(Lparse1)-1].split('m')
                    if len(Lparse1)==2:
                        time=float(Lparse1[0])*60
                    if len(Lparse2)==2:
                        time=time+float(Lparse2[0])+float(Lparse2[1])/60
                    if len(Lparse2)==1:
                        time=time+float(Lparse2[0])

                if L[0:12]=='number of k ':
                    Lparse=L.split()
                    inequiv=int(Lparse[4])
    if ecutwfc<0.1:
        raise Exception("Calculation did not complete")
    else:
        return kx, ky, kz, shiftx, shifty, shiftz, ecutwfc, energy, inequiv,time              
#extract all *.out files
    
def KconvergenceTest(fmt='*.out'):
    """
    plots energy vs # k point mesh in x, y, and z directions. If all equal, only does one plot
    KconvergenceTest('SrTiO3-260-*-*.out')

    Parameters
    ----------
    fmt : string, optional
        DESCRIPTION. The default is '*.out'. filename format for searching the working directory. This is like glob

    Returns
    -------
    None.

    """
    fmt='SrTiO3-260-*-*.out'
    dall=[]
    kx, ky, kz, shiftx, shifty, shiftz, ecutwfc, energy, inequiv,time=extractKConvergenceInfo('SrTiO3-260-0-16.out')
    
    for filepath in glob.iglob(fmt):
        print(filepath)
        try:
            d=extractKConvergenceInfo(filepath)
            dall.append(d)
        except Exception:
            print(filepath +" would not read. Check the file.")      
    
    
    df=pd.DataFrame(dall, columns=['kx', 'ky', 'kz','shiftx','shifty', 'shiftz', 'ecutwfc', 'energy','inequiv', 'time'])
    dfinal=df.sort_values('energy')
    
    mn=dfinal['energy'].min()
    dfinal.to_csv('KtestSummary.txt', header=True, index=False, sep='\t', quoting=csv.QUOTE_NONE)   
    shiftXunique=dfinal.shiftx.unique()
    shiftYunique=dfinal.shifty.unique()
    shiftZunique=dfinal.shiftz.unique()
    conv=spc.physical_constants['Rydberg constant times hc in eV'][0]
    if np.array_equal(shiftYunique,shiftXunique) and np.array_equal(shiftYunique,shiftZunique):
        L=len(shiftXunique)
        datList=[pd.DataFrame(columns=['kx', 'ky', 'kz','shiftx','shifty', 'shiftz', 'ecutwfc', 'energy','inequiv', 'time']) for i in range(L)]
        for shiftIdx in range(L):
            #loop through dfinal and put 
            for cnt in range(len(dall)):
                line=dfinal.iloc[cnt]
                if line['shiftx']==shiftXunique[shiftIdx]:
                    datList[shiftIdx]=datList[shiftIdx].append(line, ignore_index=True)
                    #if shiftIdx==1.0:
                        #print(dfinal.iloc[cnt]['kx'])
                        #print(dfinal.iloc[cnt]['shiftx'])
                        #print(datList[1])
                        
                    #print('enter')
    
        f=plt.figure()
        for shiftIdx in range(L):
            plt.plot(datList[shiftIdx]['kx'], (datList[shiftIdx]['energy']-mn)*conv, label="shift = "+ str(shiftXunique[shiftIdx]), alpha=0.7)
        plt.ylim(bottom=0)
        plt.legend()
        plt.xlabel('kx=ky=kz')
        plt.ylabel('Total Energy (eV)')  
        f.savefig('TotEvsInequivK.png')    
    else:
        print('untested code')
        LX=len(shiftXunique)
        LY=len(shiftYunique)
        LZ=len(shiftZunique)
        datListX=[pd.DataFrame(columns=['kx', 'ky', 'kz','shiftx','shifty', 'shiftz', 'ecutwfc', 'energy','inequiv', 'time']) for i in range(LX)]
        datListY=[pd.DataFrame(columns=['kx', 'ky', 'kz','shiftx','shifty', 'shiftz', 'ecutwfc', 'energy','inequiv', 'time']) for i in range(LY)]
        datListZ=[pd.DataFrame(columns=['kx', 'ky', 'kz','shiftx','shifty', 'shiftz', 'ecutwfc', 'energy','inequiv', 'time']) for i in range(LZ)]
        for shiftIdx in range(LX):
            #loop through dfinal and put 
            for cnt in range(len(dall)):
                line=dfinal.iloc[cnt]
                if line['shiftx']==shiftXunique[shiftIdx]:
                    datListX[shiftIdx]=datListX[shiftIdx].append(line, ignore_index=True)
        for shiftIdx in range(LY):
            #loop through dfinal and put 
            for cnt in range(len(dall)):
                line=dfinal.iloc[cnt]
                if line['shiftx']==shiftYunique[shiftIdx]:
                    datListY[shiftIdx]=datListY[shiftIdx].append(line, ignore_index=True)
        for shiftIdx in range(LZ):
            #loop through dfinal and put 
            for cnt in range(len(dall)):
                line=dfinal.iloc[cnt]
                if line['shiftx']==shiftZunique[shiftIdx]:
                    datListZ[shiftIdx]=datListZ[shiftIdx].append(line, ignore_index=True)
                    #if shiftIdx==1.0:
                        #print(dfinal.iloc[cnt]['kx'])
                        #print(dfinal.iloc[cnt]['shiftx'])
                        #print(datList[1])
                        
                    #print('enter')
        #plot kx
        f=plt.figure()
        for shiftIdx in range(LX):
            plt.plot(datListX[shiftIdx]['kx'], (datListX[shiftIdx]['energy']-mn)*conv, label="shift = "+ str(shiftXunique[shiftIdx]), alpha=0.7)
        plt.ylim(bottom=0)
        plt.legend()
        plt.xlabel('kx')
        plt.ylabel('Total Energy (eV)')  
        f.savefig('TotEvsshiftKx.png')
        #plot ky
        f=plt.figure()
        for shiftIdx in range(L):
            plt.plot(datListY[shiftIdx]['kx'], (datListY[shiftIdx]['energy']-mn)*conv, label="shift = "+ str(shiftYunique[shiftIdx]), alpha=0.7)
        plt.ylim(bottom=0)
        plt.legend()
        plt.xlabel('ky')
        plt.ylabel('Total Energy (eV)')  
        f.savefig('TotEvsshiftKy.png')
        #plot kz
        f=plt.figure()
        for shiftIdx in range(L):
            plt.plot(datListZ[shiftIdx]['kx'], (datListZ[shiftIdx]['energy']-mn)*conv, label="shift = "+ str(shiftZunique[shiftIdx]), alpha=0.7)
        plt.ylim(bottom=0)
        plt.legend()
        plt.xlabel('kz')
        plt.ylabel('Total Energy (eV)')  
        f.savefig('TotEvsshiftKz.png')
def importacLatticeParamEnergyFile(fname):
    '''
    

    Parameters
    ----------
    fname : TYPE
        DESCRIPTION.

    Returns
    -------
    a : float
        DESCRIPTION. lattice constant a in Bohr
    cba : float
        DESCRIPTION.c/a ratio
    totEnergy : float
        DESCRIPTION. total energy in Ry

    '''
    a=0.0
    cba=0.0
    totEnergy=0.0
    with open(fname, "r") as f:
            for line in f.readlines():
                lineStr=line.strip()
                if len(lineStr)>2:
                    if lineStr[0:2]=='ce':
                        if lineStr[7]=='1':
                            lineStr=lineStr.split()
                            a=float(lineStr[1])
                            cba=float(lineStr[5])
                    if lineStr[0]=='!':
                        lineStr=lineStr.split()
                        totEnergy=float(lineStr[4])#keep it in Ry
    return a, cba, totEnergy
#def importAllLatConstFilesInFolder(fmt):

def importAllLatParamFiles(fmt):
    """
    import all lattice parameter files. Use this for debugging any issues with plotCbAvsA. This is used in plotCbAvsA.
    Prints the filenames of all files imported to allow you to check that things import properly
    Parameters
    ----------
    fmt : str
        DESCRIPTION. Format used by glob to describe the files involved in the lattice parameter data

    Returns
    -------
    mat : numpy array of floats
        DESCRIPTION. Array of total energies
    unA : 1-d sorted numpy array
        DESCRIPTION. Array of unique values in the a-lattice parameter
    unCbA : 1-d sorted numpy array
        DESCRIPTION. Array of unique values in c/a
    data : numpy array
        DESCRIPTION. raw data extracted from files, useful for debugging

    """
    dall=[]
    for filepath in glob.iglob(fmt):
        d=importacLatticeParamEnergyFile(filepath)
        print(filepath)
        dall.append(d)            
    data=np.array(dall)
    r, c=data.shape
    unA=np.sort(np.unique(data[:,0]))
    unCbA=np.sort(np.unique(data[:,1]))
    mat=np.zeros((len(unCbA), len(unA)))
    
    for cnt in range(r):
        aData=data[cnt, 0]
        cbaData=data[cnt, 1]
        energy=data[cnt,2]
        idxA=np.searchsorted(unA, aData)
        idxCba=np.searchsorted(unCbA, cbaData)
    
        mat[idxCba, idxA]=energy
    return mat, unA, unCbA, data
    #print([idxA, idxC])
def plotCbAvsA(fmt, lim=0):
    """
    Plots C/A vs A when A is in Bohr
	fmt='graphite_*_*.out'      
	plotCbAvsA(fmt)             
    Parameters
    ----------
    fmt : str
        DESCRIPTION. Format used by glob to describe the files involved in the lattice parameter data
    lim : float, optional
        DESCRIPTION. The default is -45.599. Describes the energy threshold above which all become one color.

    Returns
    -------
    None.

    """
    mat, unA, unCbA, data=importAllLatParamFiles(fmt)

    plt.figure()
    plt.imshow(mat, origin='lower',   cmap='inferno', interpolation='spline16', vmax=lim, extent=[min(unA), max(unA), min(unCbA), max(unCbA)])
    plt.xlabel('Lattice parameter (bohr)')
    plt.ylabel('c/a ratio')
    cbar=plt.colorbar(format='%.4f')
    cbar.set_label('Total Energy (Ry)')
    plt.show()
    q=np.argmin(data[:,2])
    print("min data point: a="+ str(data[q, 0])+", c/a= "+str(data[q,1]))