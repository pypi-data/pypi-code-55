#coding=utf-8
import datetime
import struct;
import binascii

from xcommon.utils import *
from xcommon.xclient import *



# 
# 
# 

buff = XBuffer.Buffer()

payload = b"1234567890";
XClient.Xclient.packet(buff, 1, payload);

XUtil.dump(buff.array(), 0, buff.length())

buff.reset();
def testDate(buff, input):

	print('date is ', input);
	buff.putDate(input);

	buff.dump();

	dt = buff.getDate();
	print('after date is', dt);

	buff.dump();

# 2016-05-30 07:36:50.379
ts = 1464565010379 / 1000 ;
date = datetime.datetime.fromtimestamp(ts);



testDate(buff, date);


tm = datetime.datetime.now();
print('test ' , tm)
testDate(buff, tm);



buff = XBuffer.RMIBuff();
buff.put_date( tm );

tm1 = buff.get_date();
print( tm1);