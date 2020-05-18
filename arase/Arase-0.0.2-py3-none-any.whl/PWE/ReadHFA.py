import numpy as np
from ._ReadCDF import _ReadCDF
from ..Tools.CombineSpecCls import CombineSpecCls
from ..Tools.CDFEpochToUT import CDFEpochToUT
from .ReadHFAHigh import ReadHFAHigh
from .ReadHFALow import ReadHFALow

def ReadHFA(Date):
	'''
	Reads the level 2 high and low HFA data.
	
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
	
	#read the data in
	datah = ReadHFAHigh(Date)
	datal = ReadHFALow(Date)
	
	#list the fields
	fields = ['SpectraEu','SpectraEv','SpectraBgamma','SpectraEsum',
			'SpectraEr','SpectraEl','SpectraEmix','SpectraEAR']
	
	#now to combine each one
	out = {}
	for f in fields:
		out[f] = CombineSpecCls([datal[f],datah[f]])
		
	return out
	
	
		

