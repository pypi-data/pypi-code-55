import numpy as np
from ._ReadCDF import _ReadCDF
from ..Tools.SpecCls import SpecCls
from ..Tools.CDFEpochToUT import CDFEpochToUT

def ReadOmni(Date,KeV=False):
	'''
	Reads the level 2 omniflux data product for a given date.
	
	Inputs
	======
	Date : int
		Integer date in the format yyyymmdd
	Kev : bool
		Converts units to be KeV instead of eV
	
	Returns
	=======
	data : dict
		Contains the following fields:
		'Epoch' : CDF epoch
		'Date' : Date
		'ut' : UT (hours from beginning of the day)
		'Energy' : Energy bins
		'eFlux' : SpecCls object, contains electron fluxes
		
	For more information about the SpecCls object, see Arase.Tools.SpecCls 
		

	'''		
				
	#read the CDF file
	data,meta = _ReadCDF(Date,2,'omniflux')		

	if data is None:
		return None
	
	#output dict
	out = {}
	
	#get the time 
	out['Epoch'] = data['Epoch']
	out['Date'],out['ut'] = CDFEpochToUT(out['Epoch'])
	
	#the energy arrays
	out['Energy'] = data['FEDO_Energy']
	if KeV:
		out['Energy'] = out['Energy']/1000.0
	emid = np.mean(out['Energy'],axis=1)
	bw = out['Energy'][:,1,:] - out['Energy'][:,0,:]


	#replace bad data
	s = data['FEDO']
	bad = np.where(s < 0)
	s[bad] = np.nan
	if KeV:
		s = s*1000.0
	
		#plot labels
		ylabel = 'Energy (KeV)'
		zlabel = 'Omni-directional number flux (s$^{-1}$ cm$^{-2}$-sr$^{-1}$ KeV$^{-1}$)'
	else:
		
		#plot labels
		ylabel = 'Energy (eV)'
		zlabel = 'Omni-directional number flux (s$^{-1}$ cm$^{-2$-sr$^{-1}$ eV$^{-1}$)'
	
	
	#now to store the spectra
	out['eFlux'] = SpecCls(ylabel=ylabel,zlabel=zlabel,ylog=True,zlog=True)
	out['eFlux'].AddData(out['Date'],out['ut'],out['Epoch'],emid,s,Meta=meta['FEDO'],bw=bw)
		
	return out	
