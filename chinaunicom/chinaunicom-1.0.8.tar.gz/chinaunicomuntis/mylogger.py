# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime
class MyLogger:
    def __init__(self,CONFIG):
        self.PROJECT_NAME = CONFIG.get("PROJECT_NAME")
        self.LOG_PATH_DIR = CONFIG.get("LOG_PATH")
        self.LOG_FORMATTER = CONFIG.get("LOG_FORMATTER")
        self.LOG_LEVEL = CONFIG.get("LOG_LEVEL")
        self.LOG_SPLIT_TIMES = CONFIG.get("LOG_SPLIT_TIMES")
        self.mylogger = self.GetLogger()
    def GetLogger(self):#u日志通用类
    
        #日志级别
        LEVEL = logging.NOTSET
        if self.LOG_LEVEL.upper()=="INFO":
            LEVEL = logging.INFO
        if self.LOG_LEVEL.upper()=="ERROR":
            LEVEL = logging.ERROR
        if self.LOG_LEVEL.upper()=="WARNING":
            LEVEL = logging.WARNING
        if self.LOG_LEVEL.upper()=="DEBUG":
            LEVEL = logging.DEBUG
        if self.LOG_LEVEL.upper()=="CRITICAL":
            LEVEL = logging.CRITICAL
        #设置基本参数
        abspath = os.path.abspath("."+os.sep+self.PROJECT_NAME)
        #日志目录
        logFilepath = os.path.join(abspath, self.LOG_PATH_DIR)
        if not os.path.exists(logFilepath):
            os.makedirs(logFilepath)
        #文件名称
        #分割默认按照天
        SPLIT_TIMES = "%Y_%m_%d"
        if self.LOG_SPLIT_TIMES.upper() == "D":
            SPLIT_TIMES = "%Y_%m_%d"
            
        if self.LOG_SPLIT_TIMES.upper() == "H":
            SPLIT_TIMES = "%Y_%m_%d_%H"
            
        if self.LOG_SPLIT_TIMES.upper() == "M":
            SPLIT_TIMES = "%Y_%m_%d_%H_%M"
        filename = logFilepath + os.sep +'%s.log' %(datetime.now().strftime(SPLIT_TIMES))
        formatter = logging.Formatter(self.LOG_FORMATTER)
        
        #初始化
        logger = logging.getLogger()
        logger.setLevel(LEVEL)
        #文件handle
        fh = logging.FileHandler(filename, mode='a+',encoding='utf-8')
        fh.setLevel(LEVEL)  
        fh.setFormatter(formatter)
        
        #控制台handle
        ch = logging.StreamHandler()
        ch.setLevel(LEVEL)
        ch.setFormatter(formatter)
        #添加handle
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger
    def INFOLog(self,msg):
        self.mylogger.info(msg)
    def ERRORLog(self,msg):
        self.mylogger.error("\n"+\
                       "="*25+"ERROR_START"+"="*25+"\n\n"+\
                       msg+"\n"+\
                       "="*25+"ERROR_END"+"="*25+"\n")
    def WARNINGLog(self,msg):
        self.mylogger.warning("\n"+\
                       "="*25+"WARNING_START"+"="*25+"\n\n"+\
                       msg+"\n"+\
                       "="*25+"WARNING_END"+"="*25+"\n")
    def DEBUGLog(self,msg):
        self.mylogger.debug("\n"+\
                       "="*25+"DEBUG_START"+"="*25+"\n\n"+\
                       msg+"\n"+\
                       "="*25+"DEBUG_END"+"="*25+"\n")
    def CRITICALLog(self,msg):
        self.mylogger.critical("\n"+\
                       "="*25+"CRITICAL_START"+"="*25+"\n\n"+\
                       msg+"\n"+\
                       "="*25+"CRITICAL_END"+"="*25+"\n")