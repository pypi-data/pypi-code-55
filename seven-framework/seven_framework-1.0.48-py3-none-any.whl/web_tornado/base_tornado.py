# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-05-12 17:47:10
@LastEditTime: 2020-05-18 12:01:39
@LastEditors: ChenXiaolei
@Description: 基础tornado引用
"""
# 框架引用
import os
import tornado.web
import tornado.ioloop
import tornado.httpserver
import platform
from seven_framework import *
import sys
global environment
if "--production" in sys.argv:
    environment = "production"
    config_file = "config.json"
elif "--testing" in sys.argv:
    environment = "testing"
    config_file = "config_testing.json"
else:
    environment = "development"
    config_file = "config_dev.json"

sys.path.append(".local")  # 不可删除,置于其他import前
# 初始化配置,执行顺序需先于调用模块导入
config.init_config(config_file)  # 全局配置,只需要配置一次

# 初始化日志写入类调用方法
logger_error = Logger("logs/log_error", "ERROR", "log_error",
                      HostHelper.get_host_ip()).get_logger()
logger_info = Logger("logs/log_info", "INFO", "log_info",
                     HostHelper.get_host_ip()).get_logger()
