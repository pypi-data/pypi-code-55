from xcommon.utils import *
from xcommon.xclient import *

import struct;
import binascii
import types;
import datetime;
# 
# 

ENERGYGW = "00-22-12-34-56-47.MODBUS";
ENERGY_RAW = "E-1";
x = None

# class DataServicesV2:
#
# 	def sendEnergy( a, b, c):
# 		pass

f = XClient.Service('127.0.0.1', 10000);



result = f.sendEnergy( None  , ENERGYGW  ,
		ENERGY_RAW ,
		None ,
		100.0,
		None ,
		None,);


print(' result is ' + str(result));


tm = datetime.datetime.now();

try:
	result = f.alive(tm );
	print(' result is ' ,result);
except XClient.RemoteException as e:
	print(e);
	e.dump();
