# -*- coding: utf-8 -*-

from queue import Queue
from threading import *
from iqsopenapi.util import *
from enum import Enum

class EventBus(object):
    def __init__(self):
        """初始化事件管理器"""
        self.__eventQueue = Queue()
        self.__active = False
        self.__thread = Thread(target = self.__run)
        self.__handlers = {}

    def __run(self):
        """引擎运行"""
        while self.__active == True:
            try:
                event = self.__eventQueue.get()  
                self.__event_process(event)
            except Exception as e:
                logger.exception(e)

    def __event_process(self, event):
        """处理事件"""
        if event.event_type in self.__handlers:
            for handler in self.__handlers[event.event_type]:
                handler(event)

    def start(self):
        """启动"""
        self.__active = True
        self.__thread.start()

    def stop(self):
        """停止"""
        self.__active = False
        self.__thread.join()

    def add_listener(self, event_type, handler):
        """绑定事件和监听器处理函数"""
        try:
            handlerList = self.__handlers[event_type]
        except KeyError:
            handlerList = []
            self.__handlers[event_type] = handlerList
        if handler not in handlerList:
            handlerList.append(handler)

    def remove_listener(self, event_type, handler):
        """移除监听器的处理函数"""
        try:
            handlerList = self.__handlers[event_type]
            if handler in handlerList:
                handlerList.remove(handler)
            if not handlerList:
                del self.__handlers[event_type]
        except KeyError:
            pass

    def publish_event(self, event):
        """发送事件，向事件队列中存入事件"""
        self.__eventQueue.put(event)

class Event(object):
    # 事件类

    def __init__(self, event_type, **kwargs):
        self.__dict__ = kwargs
        self.event_type = event_type

    def __repr__(self):
        return ' '.join('{}:{}'.format(k, v) for k, v in self.__dict__.items())

class EVENT(Enum):
    # 系统初始化后触发

    On_Init = 'on_init'

    On_Bar = 'on_bar'

    On_Tick = 'on_tick'

    On_Order = 'on_order'

    On_Trade = 'on_trade'

    On_Scheduler = 'on_scheduler'

    On_Open = 'on_open'

    On_Close = 'on_close'