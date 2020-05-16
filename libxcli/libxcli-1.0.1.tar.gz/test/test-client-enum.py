# coding : utf-8

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
factory = XClient.Factory('127.0.0.1', 10000);
#
#


service = factory.create();

def testEnum(service):
	result = service.getType('R');
	print(' result is ' + str(result) ,  type(result));



def testSet(service):
	list = ['a','b',1];
	result = service.sendSet(list);
	print(' result is ' + str(result) ,  type(result));




def testClass(service):
	clazz = 'com.siemens.ct.its.util.lang.ClassTypeUtil' ;
	result = service.sendClass(clazz);
	print(' result is ' + str(result) ,  type(result));

# testEnum(service);
# testSet(service);
testClass(service);

