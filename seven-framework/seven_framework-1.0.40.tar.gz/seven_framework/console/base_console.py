# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-05-09 20:39:20
@LastEditTime: 2020-05-09 20:50:30
@LastEditors: ChenXiaolei
@Description: 基础控制台类
"""

from seven_framework import *
import sys
global production
production = "--production" in sys.argv
sys.path.append(".local")  # 不可删除,置于其他import前
# 初始化配置,执行顺序需先于调用模块导入
config.init_config(
    "config{0}.json".format("" if production else "_dev"))  # 全局配置,只需要配置一次

logger_error = Logger("logs/log_error", "ERROR", "log_error",
                      HostHelper.get_host_ip()).get_logger()
logger_info = Logger("logs/log_info", "INFO", "log_info",
                     HostHelper.get_host_ip()).get_logger()
