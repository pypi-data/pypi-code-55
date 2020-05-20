# coding=u8
import logging
from KE import KE
from datetime import datetime, timedelta



client = KE(host='10.1.3.63', port=7171, username='ADMIN', password='KYLIN', version=4, debug=True)

p = client.projects('learn_kylin')

m=p.models()[0]

segs=m.segments(start_time='1230000000000', end_time='1330000000000')
