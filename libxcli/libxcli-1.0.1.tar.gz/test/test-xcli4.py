from xcommon.utils import *
from xcommon.xclient import *
from xcommon.xclient import Xserialization;

import struct;
import binascii
import types;
import datetime;
# #
# #
#
#
f = XClient.Service('127.0.0.1', 10000);
#
#

# result = f.sendListData2(  [ 1,2,3,4.33,'aaaaaaaa', [3,5]]); # 1,2,3,4.33,'aaaaaaaa',


# result = f.sendMap( {'a':1,'b':'bbbbbbbb' , 2:3 , 2.11: 'aaaaaaaaaa', 'list':[1,2,3,4]});
#
#
# print(' result is ' + str(result));
#
#
# result = f.sendMap1( {'a':1,'b':'bbbbbbbb' , 1:22, 'list':[1,2,3,4]});
#
#
# print(' result is ' + str(result));
#
#
#
# result = f.sendMap2( {'a':1,'b':'bbbbbbbb' , 1:22, 'list':[1,2,3,4]});
#
#
# print(' result is ' + str(result));
#
#
#
# result = f.sendMap3( {'100':1,'22':'bbbbbbbb' , 1:22, '22555':[1,2,3,4]});
#
#
# print(' result is ' + str(result));
#
#
#
#
# result = f.getBean( 'aaaaaaaaa');
#
#
# print(' result is ' + str(result));
#


bean = Xserialization.Bean('com.siemens.ct.its.bt.test.TestServiceV2MockImpl$MyName');
bean['name'] = 'aaaa' ;


result = f.setBean( bean );


print(' result is ' + str(result) ,  type(result));


