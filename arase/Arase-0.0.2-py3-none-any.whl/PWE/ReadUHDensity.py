import numpy as np
from ._ReadCDF import _ReadCDF
from ..Tools.CDFEpochToUT import CDFEpochToUT

def ReadUHDensity(Date):
	'''
	Reads density measured using UH frequency.
	
	Inputs
	======
	Date : int
		Integer date in the format yyyymmdd
	
	Returns
	=======
	data : numpy.recarray
		Contains the following fields:
				'Date' : int32
				'ut' : float32
				'Epoch' : int64
				'Density' : float32
				'Fuh' : float32
				'Quality' : int32
		

	'''	

	#read the CDF file
	data,meta = _ReadCDF(Date,'hfa',3,'')		

	if data is None:
		return None

	#create output array
	dtype = [	('Date','int32'),
				('ut','float32'),
				('Epoch','int64'),
				('Density','float32'),
				('Fuh','float32'),
				('Quality','int32')]
	n = data['Epoch'].size
	out = np.recarray(n,dtype=dtype)
	
	#get the data
	out.Date,out.ut = CDFEpochToUT(data['Epoch'])
	out.Epoch = data['Epoch']
	out.Density = data['ne_mgf']
	out.Fuh = data['Fuhr']
	out.Quality = data['quality_flag']
	
	return out
	
				
