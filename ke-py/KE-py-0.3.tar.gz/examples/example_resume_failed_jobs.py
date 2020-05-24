# coding=u8
from KE import KE
from datetime import datetime, timedelta


client = KE('solution-3', port=7099, username='ADMIN', password='KYLIN', version=3)

"""
定时监控Job，将失败的job重启
"""

# 过滤出失败的job
failed_jobs = client.jobs(time_filter=4, status=8)

for job in failed_jobs:
    print('restarting failed job: %s' % job.id)
    job.resume()



