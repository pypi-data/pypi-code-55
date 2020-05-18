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
		'EpochTOF' : CDF epoch
		'Date' : Date
		'DateTOF' : Date
		'ut' : UT (hours from beginning of the day)
		'utTOF' : UT (hours from beginning of the day)
		'Energy' : Energy bins
		'H+Flux' : SpecCls object, contains proton fluxes
		'He++Flux' : SpecCls object, contains helium ++ ion fluxes
		'He+Flux' : SpecCls object, contains helium ion fluxes
		'O++Flux' : SpecCls object, contains oxygen ++ ion fluxes
		'O+Flux' : SpecCls object, contains oxygen ion fluxes
		'O2+Flux' : SpecCls object, contains molecular oxygen ion fluxes
		'H+FluxTOF' : SpecCls object, contains proton fluxes
		'He++FluxTOF' : SpecCls object, contains helium ++ ion fluxes
		'He+FluxTOF' : SpecCls object, contains helium ion fluxes
		'O++FluxTOF' : SpecCls object, contains oxygen ++ ion fluxes
		'O+FluxTOF' : SpecCls object, contains oxygen ion fluxes
		'O2+FluxTOF' : SpecCls object, contains molecular oxygen ion fluxes
		
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
	out['EpochTOF'] = data['epoch_tof']
	out['DateTOF'],out['utTOF'] = CDFEpochToUT(out['EpochTOF'])
	
	#the energy arrays
	out['Energy'] = data['FIDO_Energy']
	

	#replace bad data
	fields = {	'FPDO' : 		('H+Flux','Energy (keV/q)','Omni-directional H$^+$ flux (#/s-cm2-sr-keV/q)'),
				'FHE2DO' : 		('He++Flux','Energy (keV/q)','Omni-directional He$^{++}$ flux (#/s-cm2-sr-keV/q)'),
				'FHEDO' : 		('He+Flux','Energy (keV/q)','Omni-directional He$^+$ flux (#/s-cm2-sr-keV/q)'),
				'FOPPDO' : 		('O++Flux','Energy (keV/q)','Omni-directional O$^{++}$ flux (#/s-cm2-sr-keV/q)'),
				'FODO' : 		('O+Flux','Energy (keV/q)','Omni-directional O$^+$ flux (#/s-cm2-sr-keV/q)'),
				'FO2PDO' : 		('O2+Flux','Energy (keV/q)','Omni-directional O$_2^+$ flux (#/s-cm2-sr-keV/q)'),
				'FPDO_tof' : 	('H+FluxTOF','Energy (keV/q)','Omni-directional H$^+$ Flux for TOF data (#/s-cm2-sr-keV/q)'),
				'FHE2DO_tof' : 	('He++FluxTOF','Energy (keV/q)','Omni-directional He$^{++}$ Flux for TOF data (#/s-cm2-sr-keV/q)'),
				'FHEDO_tof' : 	('He+FluxTOF','Energy (keV/q)','Omni-directional He$^+$ Flux for TOF data (#/s-cm2-sr-keV/q)'),
				'FOPPDO_tof' : 	('O++FluxTOF','Energy (keV/q)','Omni-directional O$^{++}$ Flux for TOF data (#/s-cm2-sr-keV/q)'),
				'FODO_tof' : 	('O+FluxTOF','Energy (keV/q)','Omni-directional O$^+$ Flux for TOF data (#/s-cm2-sr-keV/q)'),
				'FO2PDO_tof' : 	('O2+FluxTOF','Energy (keV/q)','Omni-directional O$_2^+$ Flux for TOF data (#/s-cm2-sr-keV/q)') }
	
	for k in list(fields.keys()):
		s = data[k]
		bad = np.where(s < 0)
		s[bad] = np.nan
		
		field,ylabel,zlabel = fields[k]
		
		#now to store the spectra
		if not '_tof' in k:
			out[field] = SpecCls(ylabel=ylabel,zlabel=zlabel,ylog=True,zlog=True)
			out[field].AddData(out['Date'],out['ut'],out['Epoch'],out['Energy'],s,Meta=meta[k])
		else:
			out[field] = SpecCls(ylabel=ylabel,zlabel=zlabel,ylog=True,zlog=True)
			out[field].AddData(out['DateTOF'],out['utTOF'],out['EpochTOF'],out['Energy'],s,Meta=meta[k])
			
	return out	
