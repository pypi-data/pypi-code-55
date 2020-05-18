import numpy as np
from ._ReadCDF import _ReadCDF
from ..Tools.SpecCls import SpecCls
from ..Tools.CDFEpochToUT import CDFEpochToUT

def ReadOmni(Date):
	'''
	Reads the level 2 omniflux data product for a given date.
	
	Inputs
	======
	Date : int
		Integer date in the format yyyymmdd
	
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
	out['Epoch'] = data['epoch']
	out['Date'],out['ut'] = CDFEpochToUT(out['Epoch'])
	
	#the energy arrays
	out['Energy'] = data['FEDO_Energy']
	

	#replace bad data
	s = data['FEDO']
	bad = np.where(s < 0)
	s[bad] = np.nan
	
	#plot labels
	ylabel = 'Energy (keV)'
	zlabel = 'Omni-directional Electron Flux (cm$^{-2}$ s$^{-1}$ sr$^{-1}$ keV$^{-1}$)'
	
	
	#now to store the spectra
	out['eFlux'] = SpecCls(ylabel=ylabel,zlabel=zlabel,ylog=True,zlog=True)
	out['eFlux'].AddData(out['Date'],out['ut'],out['Epoch'],out['Energy'],s,Meta=meta['FEDO'])
		
	return out	
