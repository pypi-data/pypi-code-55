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
		'EpochL' : CDF epoch
		'EpochH' : CDF epoch
		'DateL' : Date
		'DateH' : Date
		'utL' : UT (hours from beginning of the day)
		'utH' : UT (hours from beginning of the day)
		'EnergyL' : Energy bins
		'EnergyH' : Energy bins
		'eFluxL' : SpecCls object, contains electron fluxes
		'eFluxH' : SpecCls object, contains electron fluxes
		
	For more information about the SpecCls object, see Arase.Tools.SpecCls 
		

	'''	
				
	#read the CDF file
	data,meta = _ReadCDF(Date,2,'omniflux')		

	if data is None:
		return None	

	#output dict
	out = {}
	
	#get the time 
	out['EpochL'] = data['Epoch_L']
	out['DateL'],out['utL'] = CDFEpochToUT(out['EpochL'])
	out['EpochH'] = data['Epoch_H']
	out['DateH'],out['utH'] = CDFEpochToUT(out['EpochH'])
	
	#the energy arrays
	out['EnergyL'] = data['FEDO_L_Energy']
	out['EnergyH'] = data['FEDO_H_Energy']
	
	#get the midpoints
	eL = np.mean(out['EnergyL'],axis=0)
	eH = np.mean(out['EnergyH'],axis=0)
	
	#replace bad data
	L = data['FEDO_L']
	bad = np.where(L < 0)
	L[bad] = np.nan
	
	H = data['FEDO_H']
	bad = np.where(H < 0)
	H[bad] = np.nan
	
	#labels
	zlabelH = 'Omni-directional flux of HEP-H (1/keV-sr-s-cm$^2$)'
	zlabelL = 'Omni-directional flux of HEP-L (1/keV-sr-s-cm$^2$)'
	ylabelH = 'Energy (keV)'
	ylabelL = 'Energy (keV)'
	
	
	#now to store the spectra
	out['eFluxL'] = SpecCls(ylabel=ylabelL,zlabel=zlabelL,ylog=True,zlog=True,ScaleType='positive')
	out['eFluxL'].AddData(out['DateL'],out['utL'],out['EpochL'],eL,L,bw=None,dt=None,Meta=meta['FEDO_L'])
	
	out['eFluxH'] = SpecCls(ylabel=ylabelH,zlabel=zlabelH,ylog=True,zlog=True,ScaleType='positive')
	out['eFluxH'].AddData(out['DateH'],out['utH'],out['EpochH'],eH,H,bw=None,dt=None,Meta=meta['FEDO_H'])
		
	return out	
