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
service = XClient.Service('127.0.0.1', 10000, service="/admin");
#
#



build  = Xserialization.Bean('com.siemens.ct.its.bt.pojo.cmdb.Building');
build['name'] = 'aaaa' ;
build['buildId'] = 'AICIAKKEKF' ;
build['fullName'] = 'fullName' ;
build['siteId']  = 25 ;
build['buildId'] = 'AICIAKKEKF' ;
build['buildId'] = 'AICIAKKEKF' ;




build = service.saveBuilding( build);
# sites = service.getSites();
#
# for site in sites:
# 	site.id ==

print(' result is ' + str(build) ,  type(build));


