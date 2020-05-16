from xcommon.utils import *
from xcommon.xclient import *

import struct;
import binascii
import types;
# 
# 

ENERGYGW = "00-22-12-34-56-47.MODBUS";
ENERGY_RAW = "E-1";

x = None 
try:

	

	f = XClient.MetaFactoryFile('./DataServicesV2.json');

	meta = f.loadMeta();

	method = meta.getMethod('sendEnergy');


	x = XClient.XclientV2();

	x.connect('127.0.0.1', 10000);

 	
	SERVICE_NAME = "/Data2";
	# ifcpID , gwId rawId timestamp
	params = ( None  , ENERGYGW  , 
		ENERGY_RAW , 
		'aaa' ,
		100.0,
		None , 
		None,);
	
	buff = x.remoteCall(  SERVICE_NAME  , method ,  params );
	print(buff);
	XUtil.dump(buff, 0, len(buff)); #.dump();
	

	
	
except XClient.RemoteException as e:
	print(e);
	e.dump();
	
	
	
	
finally:
	x.close();

