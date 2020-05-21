# -*- coding: utf-8 -*-

from iqsopenapi import *

config = {
  "base": {
    "start_date": "2016-06-01",
    "end_date": "2016-12-01",
    "benchmark": "000300.XSHG",
    "accounts": {
      "stock": 100000
    }
  },
  "extra": {
    "log_level": "verbose",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": True
    }
  }
}

strategy_file_path = r'D:\gitwork\inquantstudio\IQSOpenApi\IQS.OpenApi.Python\iqsopenapi\example\teststrategy.py'

run_file(strategy_file_path, config)
