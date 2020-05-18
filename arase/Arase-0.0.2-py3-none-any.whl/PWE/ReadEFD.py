import numpy as np
from ._ReadCDF import _ReadCDF
from ..Tools.SpecCls import SpecCls
from ..Tools.CDFEpochToUT import CDFEpochToUT

def ReadEFD(Date):
	'''
	Reads the level 2 EFD part of PWE data.
	
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
		'F' : Frequency bins
		'F100' : Frequency bins
		'Spectra' : SpecCls object, contains Spectra
		'SpectraEvEv' : SpecCls object, contains Spectra
		'SpectraEuEu' : SpecCls object, contains Spectra
		'SpectraEuEvRe' : SpecCls object, contains Spectra
		'SpectraEuEvIm' : SpecCls object, contains Spectra
		
	For more information about the SpecCls object, see Arase.Tools.SpecCls 
		

	'''		

	#List the fields to output
	fields = {	'spectra' : 		('Spectra','Frequency, $f$ (Hz)',r'EFD spectrum, $E_v$ ((mV/m)$^2$/Hz)'),
				'spectra_EvEv' : 	('SpectraEvEv','Frequency, $f$ (Hz)',r'EFD spectrum, $\Re(E_v)^2+\Im(E_v)^2$ ((mV/m)$^2$/Hz)'),
				'spectra_EuEu' : 	('SpectraEuEu','Frequency, $f$ (Hz)',r'EFD spectrum, $\Re(E_u)^2+\Im(E_u)^2$ ((mV/m)$^2$/Hz)'),
				'spectra_EuEv_re' : ('SpectraEuEvRe','Frequency, $f$ (Hz)',r'EFD spectrum, $\Re(E_u)\Re(E_v)+\Im(E_u)\Im(E_v)$ ((mV/m)$^2$/Hz)'),
				'spectra_EuEv_im' : ('SpectraEuEvIm','Frequency, $f$ (Hz)',r'EFD spectrum, $\Re(E_u)\Im(E_v)+\Im(E_u)\Re(E_v)$ ((mV/m)$^2$/Hz)'),}
				
	#read the CDF file
	data,meta = _ReadCDF(Date,'efd',2,'spec')		
	
	#output dict
	out = {}
	
	if data is None:
		return None
		
	#get the time 
	out['Epoch'] = data['Epoch']
	out['Date'],out['ut'] = CDFEpochToUT(out['Epoch'])
	
	#the frequency arrays
	out['F'] = data['frequency']
	out['F100'] = data['frequency_100hz']
			
	#now to store the spectra
	for k in list(fields.keys()):
		spec = data[k]
		bad = np.where(spec < 0)
		spec[bad] = np.nan
		field,ylabel,zlabel = fields[k]
		f = data[meta[k]['DEPEND_1']]
		if meta[k]['DEPEND_1'] == 'frequency':
			bw = data['band_width']
		else:
			bw = np.ones(f.size,dtype='float32')
		out[field] = SpecCls(ylabel=ylabel,zlabel=zlabel,ScaleType='positive')
		out[field].AddData(out['Date'],out['ut'],out['Epoch'],f,spec,Meta=meta[k],dt=1.0,bw=bw)
		
	return out	
				
				
	
