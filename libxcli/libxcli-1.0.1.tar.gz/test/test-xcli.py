from xcommon.utils import *
from xcommon.xclient import *

import traceback;
import struct;
import binascii
import types;
# 
# 


print(type(1));



CMD = 9 ;
x = None ;
try:
	x = XClient.Xclient();

	x.connect('127.0.0.1', 10000);

	buff = x.execute( CMD , None);
	
	XUtil.dump(buff, 0, len(buff)); #.dump();
	
	
	
	
	
except XClient.RemoteException as e:
	print(e);
	e.dump();
except Exception as e:
	print(e);
	exstr = traceback.format_exc()
	print(exstr);
	
finally:
	x.close();

