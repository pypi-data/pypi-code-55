import numpy as np
from ._ReadCDF import _ReadCDF
from ..Tools.CDFEpochToUT import CDFEpochToUT

def ReadMGF(Date):
	'''
	Reads the level 2 8sec data product for a given date.
	
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
				'BxGSE' : float32
				'ByGSE' : float32
				'BzGSE' : float32
				'BxGSM' : float32
				'ByGSM' : float32
				'BzGSM' : float32
				'BxSM' : float32
				'BySM' : float32
				'BzSM' : float32
				'B' : float32	
		

	'''	

	#read the CDF file
	data,meta = _ReadCDF(Date,2,'8sec')		

	if data is None:
		return None

	#create output array
	dtype = [	('Date','int32'),
				('ut','float32'),
				('Epoch','int64'),
				('BxGSE','float32'),
				('ByGSE','float32'),
				('BzGSE','float32'),
				('BxGSM','float32'),
				('ByGSM','float32'),
				('BzGSM','float32'),
				('BxSM','float32'),
				('BySM','float32'),
				('BzSM','float32'),
				('B','float32')]	
				
	n = data['epoch_8sec'].size
	out = np.recarray(n,dtype=dtype)
	
	#get the data
	out.Date,out.ut = CDFEpochToUT(data['epoch_8sec'])
	out.Epoch = data['epoch_8sec']

	#copy the various fields across
	out.B = data['magt_8sec']
	out.BxGSE = data['mag_8sec_gse'][:,0]
	out.ByGSE = data['mag_8sec_gse'][:,1]
	out.BzGSE = data['mag_8sec_gse'][:,2]
	out.BxGSM = data['mag_8sec_gsm'][:,0]
	out.ByGSM = data['mag_8sec_gsm'][:,1]
	out.BzGSM = data['mag_8sec_gsm'][:,2]
	out.BxSM = data['mag_8sec_sm'][:,0]
	out.BySM = data['mag_8sec_sm'][:,1]
	out.BzSM = data['mag_8sec_sm'][:,2]
	
	for f in out.dtype.names:
		if 'B' in f:
			bad = np.where(out[f] == -1e+31)[0]
			out[f][bad] = np.nan
	
	return out
	
				
