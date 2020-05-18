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
		'EnergySSD' : SSD Energy bins
		'EnergyGSO' : GSO Energy bins
		'eFluxSSD' : SpecCls object, contains SSD electron fluxes
		'eFluxGSO' : SpecCls object, contains GSO electron fluxes
		
	For more information about the SpecCls object, see Arase.Tools.SpecCls 
		

	'''		
				
		
	#read the CDF file
	data,meta = _ReadCDF(Date,2,'omniflux')		
	
	#output dict
	out = {}
	
	if data is None:
		return None
	
	#get the time 
	out['Epoch'] = data['Epoch']
	out['Date'],out['ut'] = CDFEpochToUT(out['Epoch'])
	
	#the energy arrays
	out['EnergySSD'] = data['FEDO_SSD_Energy']
	out['EnergyGSO'] = data['FEDO_GSO_Energy']
	
	#get the midpoints
	essd = np.mean(out['EnergySSD'],axis=0)
	egso = np.mean(out['EnergyGSO'],axis=0)
	
	#replace bad data
	ssd = data['FEDO_SSD']
	bad = np.where(ssd < 0)
	ssd[bad] = np.nan
	
	gso = data['FEDO_GSO']
	bad = np.where(gso < 0)
	gso[bad] = np.nan
	
	#plot labels
	zlabelS = 'Omni-directional flux of XEP SSD (1/keV-sr-s-cm$^2$)'
	ylabelS = 'Energy (keV)'
	zlabelG = 'Omni-directional flux of XEP GSO (1/keV-sr-s-cm$^2$)'
	ylabelG = 'Energy (keV)'
	
	
	#now to store the spectra
	out['eFluxSSD'] = SpecCls(ylabel=ylabelS,zlabel=zlabelS,ylog=True,zlog=True,ScaleType='positive')
	out['eFluxSSD'].AddData(out['Date'],out['ut'],out['Epoch'],essd,ssd,Meta=meta['FEDO_SSD'])
	out['eFluxGSO'] = SpecCls(ylabel=ylabelG,zlabel=zlabelG,ylog=True,zlog=True,ScaleType='positive')
	out['eFluxGSO'].AddData(out['Date'],out['ut'],out['Epoch'],egso,gso,Meta=meta['FEDO_GSO'])
		
	return out	
