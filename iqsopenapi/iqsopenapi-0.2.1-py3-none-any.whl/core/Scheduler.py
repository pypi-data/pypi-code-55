# -*- coding: utf-8 -*-
from iqsopenapi.core.events import *
import types

class Scheduler(object):

    def __init__(self,event_bus):
        self.__tasks = []
        self.__th = None
        self.__event_bus = event_bus

    def add_task(self,task):
        """添加定时任务"""
        if not task:
            return False
        if self.__th is None:
            self.__th = threading.Thread(target=self.__run)
            self.__th.setDaemon(True)
            self.__th.start()
        self.__tasks.append(task)
        
    def __run(self):
        """定时任务回调"""
        while(True):
            try:
                for task in self.__tasks:
                    task.raise_event_on_time(self.__event_bus)
            except Exception as e:
                logger.exception(e)
            time.sleep(0.2)

class SchedulerTask(object):

    def __init__(self, func,time,event_type,*args):
        self.__func = func
        self.__time = time
        self.__event_type = event_type
        self.__args = args
        self.pre_execute_time = None

    def raise_event_on_time(self,event_bus):
        now = datetime.datetime.now()
        timeStr = now.strftime('%Y%m%d%H%M%S')
        if self.pre_execute_time is not None and self.pre_execute_time.strftime('%Y%m%d%H%M%S') == timeStr:
            return
        if(isinstance(self.__time,datetime.datetime)):
            if self.__time.strftime('%Y%m%d%H%M%S') == timeStr:
                self.__raise_event(now,event_bus)
        elif(isinstance(self.__time,datetime.time)):
            if self.__time.strftime('%H%M%S') == now.strftime('%H%M%S'):
                self.__raise_event(now,event_bus)

    def __raise_event(self,raise_time,event_bus):
        task_event = Event(self.__event_type,func = self.__func,raise_time = raise_time,args = self.__args)
        event_bus.publish_event(task_event)
        self.pre_execute_time = raise_time
        logger.info('run scheduler:' + raise_time.strftime('%Y%m%d%H%M%S'))