import numpy as np
from ..LEPi.ReadOmni import ReadOmni as LEP 
from ..MEPi.ReadOmni import ReadOmni as MEP 

from ..Tools.CombineSpecCls import CombineSpecCls
from ..Tools.CDFEpochToUT import CDFEpochToUT

def ReadOmni(Date,Instruments=['LEPi','MEPi']):
	'''
	Get a SpecCls object containing all of the electron data in one place.
	
	'''

	
	DataH = []
	DataHe = []
	DataO = []
	
	if 'LEP' in Instruments or 'LEPi' in Instruments:
		#Add LEP spectra
		tmp = LEP(Date)
		
		if not len(list(tmp.keys())) == 0:
			DataH.append(tmp['H+Flux'])
			DataHe.append(tmp['He+Flux'])
			DataO.append(tmp['O+Flux'])
			
			
			
	if 'MEP' in Instruments or 'MEPi' in Instruments:
		#Add MEP spectra
		tmp = MEP(Date)
		
		if not len(list(tmp.keys())) == 0:
			DataH.append(tmp['H+Flux'])
			DataHe.append(tmp['He+Flux'])
			DataO.append(tmp['O+Flux'])			
				
	return CombineSpecCls(DataH),CombineSpecCls(DataHe),CombineSpecCls(DataO)
