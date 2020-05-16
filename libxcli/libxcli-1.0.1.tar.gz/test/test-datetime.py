#coding=utf-8
import datetime


tm = datetime.datetime.now();

print(tm);
print(tm.timestamp());


# 2016-05-30 07:36:50.379
ts = 1464565010379 / 1000 ;
date = datetime.datetime.fromtimestamp(ts);

print(date);


