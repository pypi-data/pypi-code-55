from xcommon.utils import *
from xcommon.xclient import *

import struct;
import binascii
import types;
# 
# 

# f = XClient.MetaFactoryFile('./DataServicesV2.json');
#
# meta = f.loadMeta();
#
# print(str(meta));


b1 = b'1234567890';
b2 = None;
b2 = bytearray(40);

b2[4:4+len(b1)]= b1

print(b1);
print(id(b1));

print(b2);
print(id(b2));
print(len(b2));
#
# #
x = None;

x = XClient.Xclient('127.0.0.1', 10000);

x.connect();


f = XClient.MetaFactoryRemote(x);

meta = f.loadMeta();

print(str(meta));
