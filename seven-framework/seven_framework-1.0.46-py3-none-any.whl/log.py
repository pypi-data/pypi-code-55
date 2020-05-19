# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-04-16 21:32:43
@LastEditTime: 2020-04-21 19:15:17
@LastEditors: ChenXiaolei
@Description: 
"""

import logging
import logging.handlers
import time
import os
import json
import socket
import platform

class Logger:
    """
    指定保存日志的文件路径，日志级别，以及调用文件 将日志存入到指定的文件中
    级别优先级:NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL
    """
    def __init__(self, log_file_name, log_level, logger, host_ip="", project_name=None):
        """
        @description: 
        @param log_file_name: 日志存储文件路径
        @param log_level: 日志等级
        @param logger: 日志标识
        @param host_ip: 服务器IP
        @param project_name: 项目标志
        @last_editors: ChenXiaolei
        """
        if not project_name:
            if platform.system() == "Windows":
                project_name = os.getcwd().split('\\')[-1]
            else:
                project_name = os.getcwd().split('/')[-1]

        # 判断文件夹是否存在，不存在则创建
        path_list = log_file_name.split("/")
        path_log = log_file_name[0:log_file_name.find(path_list[len(path_list)
                                                                - 1])]
        if not os.path.isdir(path_log):
            os.mkdir(path_log)

        logging_level = ''

        if log_level.upper() == 'NOTSET':
            logging_level = logging.NOTSET
        elif log_level.upper() == 'DEBUG':
            logging_level = logging.DEBUG
        elif log_level.upper() == 'INFO':
            logging_level = logging.INFO
        elif log_level.upper() == 'WARNING':
            logging_level = logging.WARNING
        elif log_level.upper() == 'ERROR':
            logging_level = logging.ERROR
        elif log_level.upper() == 'CRITICAL':
            logging_level = logging.CRITICAL

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging_level)

        # 创建handler，用于写入日志文件
        self.handler_file = logging.handlers.TimedRotatingFileHandler(
            log_file_name, 'D', 1, 10)
        self.handler_file.suffix = "%Y%m%d.log"  # 设置 切分后日志文件名的时间格式 默认 log_file_name+"." + suffix 如果需要更改需要改logging 源码
        self.handler_file.setLevel(logging_level)

        formatter = logging.Formatter(
            json.dumps({
                "record_time": "%(asctime)s",
                "level": "%(levelname)s",
                "log_msg": "%(message)s",
                "host_ip": host_ip,
                "project_name": project_name
            }))
        self.handler_file.setFormatter(formatter)

        # 创建handler，用于输出至控制台
        # 定义控制台输出handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s][%(name)s][%(levelname)s]%(message)s')
        self.handler_console = logging.StreamHandler() # 输出到控制台的handler
        self.handler_console.setFormatter(formatter)
        
        # 给logger添加handler
        if not self.logger.handlers:
            self.logger.addHandler(self.handler_file)
            self.logger.addHandler(self.handler_console)

    def close(self):
        self.logger.removeHandler(self.handler_file)
        self.handler_file.close()

    def get_logger(self):
        return self.logger

    @classmethod
    def get_logger_by_name(self, loger_name):
        """
        @description: 通过日志标识获取logger
        @param loger_name: 日志标识
        @return: logger
        @last_editors: ChenXiaolei
        """
        return logging.getLogger(loger_name)
