from xcommon.utils import *
from xcommon.xclient import *

import struct;
import binascii
import types;
import datetime;
#
import re;

from xcommon.xclient import Xserialization


def testParse(input):
	val = Xserialization.parseTypes(input);
	print( input , '==>', val);


testParse('List');
testParse('Map');
testParse('List<>');
testParse('List<Object>');
testParse('Map<>');

testParse('List<string>');
testParse('Map<type1,type2>');
testParse('List<Map>');
testParse('List<Map<type1,type2>>');