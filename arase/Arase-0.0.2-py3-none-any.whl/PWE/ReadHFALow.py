import numpy as np
from ._ReadCDF import _ReadCDF
from ..Tools.SpecCls import SpecCls
from ..Tools.CDFEpochToUT import CDFEpochToUT

def ReadHFALow(Date):
	'''
	Reads the level 2 low HFA data.
	
	Inputs
	======
	Date : int
		Integer date in the format yyyymmdd
	
	Returns
	=======
	data : dict
		Contains the following fields:
		'EpochH' : CDF epoch
		'DateH' : Date
		'utH' : UT (hours from beginning of the day)
		'FH' : Frequency bins
		'EpochL' : CDF epoch
		'DateL' : Date
		'utL' : UT (hours from beginning of the day)
		'FL' : Frequency bins
		'SpectraEu' : SpecCls object, contains Spectra
		'SpectraEv' : SpecCls object, contains Spectra
		'SpectraBgamma' : SpecCls object, contains Spectra
		'SpectraEsum' : SpecCls object, contains Spectra
		'SpectraEr' : SpecCls object, contains Spectra
		'SpectraEl' : SpecCls object, contains Spectra
		'SpectraEmix' : SpecCls object, contains Spectra
		'SpectraEAR' : SpecCls object, contains Spectra
		
	For more information about the SpecCls object, see Arase.Tools.SpecCls 
		

	'''		
		
	#List the fields to output
	fields = {	'spectra_eu' : 		('SpectraEu','Frequency, $f$ (kHz)','Power spectra $E_u^2$ (mV$^2$/m$^2$/Hz)'),
				'spectra_ev' : 		('SpectraEv','Frequency, $f$ (kHz)','Power spectra $E_v^2$ (mV$^2$/m$^2$/Hz)'),
				'spectra_bgamma' : 	('SpectraBgamma','Frequency, $f$ (kHz)','Power spectra $B_{\gamma}^2$ (pT$^2$/Hz)'),
				'spectra_esum' : 	('SpectraEsum','Frequency, $f$ (kHz)','Power spectra $E_u^2 + E_v^2$ (mV$^2$/m$^2$/Hz)'),
				'spectra_er' : 		('SpectraEr','Frequency, $f$ (kHz)','Power spectra $E_{right}^2$ (mV$^2$/m$^2$/Hz)'),
				'spectra_el' : 		('SpectraEl','Frequency, $f$ (kHz)','Power spectra $E_{left}^2$ (mV$^2$/m$^2$/Hz)'),
				'spectra_e_mix' : 	('SpectraEmix','Frequency, $f$ (kHz)','Power spectra $E_u^2$ or $E_v^2$ or $E_u^2 + E_v^2$ (mV$^2$/m$^2$/Hz)'),
				'spectra_e_ar' : 	('SpectraEAR','Frequency, $f$ (kHz)','Spectra Axial Ratio LH:-1/RH:+1'),}
				
	#read the CDF file
	data,meta = _ReadCDF(Date,'hfa',2,'low')		

	if data is None:
		return None
	
	#output dict
	out = {}
	
	#get the time 
	out['Epoch'] = data['Epoch']
	out['Date'],out['ut'] = CDFEpochToUT(out['Epoch'])
	
	#the frequency arrays
	out['F'] = data['freq_spec']
			
	#now to store the spectra
	for k in list(fields.keys()):
		spec = data[k]

		field,ylabel,zlabel = fields[k]
		if k == 'spectra_e_ar':
			ScaleType = 'range'
		else:
			ScaleType = 'positive'
		bad = np.where(spec == -999.9)
		spec[bad] = np.nan
		out[field] = SpecCls(ylabel=ylabel,zlabel=zlabel,ScaleType=ScaleType)
		out[field].AddData(out['Date'],out['ut'],out['Epoch'],out['F'],spec,Meta=meta[k],dt=data['time_step']/3600.0)
		
	return out	
