from .. import Globals
import numpy as np
from ..Tools.Downloading._DownloadData import _DownloadData

def DownloadData(prod,StartYear=2016,EndYear=2019,Overwrite=False):
	'''
	Downloads Arase position data.

	prod : 'l3' or 'def'
	
	'''
	url0 = 'https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/satellite/erg/orb/{:s}/'.format(prod)
	vfmt = ['v']	
	idxfname = Globals.DataPath + 'Pos/Index-{:s}.dat'.format(prod)
	datapath = Globals.DataPath + 'Pos/{:s}/'.format(prod)
		
	if StartYear == 2016 and prod == 'l3':
		url16 = url0 + '{:04d}/tmp/'
		_DownloadData(url16,idxfname,datapath,2016,2016,vfmt,Overwrite)
		StartYear = 2017
	
	url0 += '{:04d}/'
	_DownloadData(url0,idxfname,datapath,StartYear,EndYear,vfmt,Overwrite)
	
