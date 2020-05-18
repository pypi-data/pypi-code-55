import numpy as np
from ..LEPe.ReadOmni import ReadOmni as LEP 
from ..MEPe.ReadOmni import ReadOmni as MEP 
from ..HEP.ReadOmni import ReadOmni as HEP 
from ..XEP.ReadOmni import ReadOmni as XEP 
from ..Tools.CombineSpecCls import CombineSpecCls
from ..Tools.CDFEpochToUT import CDFEpochToUT

def ReadOmni(Date,Instruments=['LEPe','MEPe','HEP','XEP']):
	'''
	Get a SpecCls object containing all of the electron data in one place.
	
	'''

	
	Data = []
	
	if 'LEP' in Instruments or 'LEPe' in Instruments:
		#Add LEP spectra
		tmp = LEP(Date,KeV=True)
		
		if not len(list(tmp.keys())) == 0:
			Data.append(tmp['eFlux'])
			
			
			
	if 'MEP' in Instruments or 'MEPe' in Instruments:
		#Add MEP spectra
		tmp = MEP(Date)
		
		if not len(list(tmp.keys())) == 0:
			Data.append(tmp['eFlux'])
			
			
	if 'HEP' in Instruments:
		#Add HEP spectra
		tmp = HEP(Date)
		
		if not len(list(tmp.keys())) == 0:
			Data.append(tmp['eFluxL'])
			Data.append(tmp['eFluxH'])


			
	if 'XEP' in Instruments:
		#Add XEP spectra
		tmp = XEP(Date)
		
		if not len(list(tmp.keys())) == 0:
			Data.append(tmp['eFluxSSD'])
			
	return CombineSpecCls(Data)
