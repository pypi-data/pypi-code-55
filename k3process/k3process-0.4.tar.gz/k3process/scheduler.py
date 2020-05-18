'''
Schedule synchronous and asynchronous tasks
'''

import queue
import datetime
import threading
import time
import logging

HIGH = -5
NORMAL = 0
LOW = 5

logger = logging.getLogger(__name__)

class SchedulerException(Exception):
    pass

class SchedulerStoppedException(SchedulerException):
    pass

class SchedulerFullException(SchedulerException):
    pass

class Scheduler():
    ''' This class has the tools to run a queue of scheduled tasks synchronously or asynchronously '''
    
    def __init__(self, maxTasks):
        ''' Initialization of the scheduler.
        
        :param maxTasks: The maximum number of tasks that the scheduler can queue. 
        
        '''
        self.tasks = queue.PriorityQueue(maxTasks)
        self.repeatedTasks = []
        self.repeatedTaskLastExe = {}
        self.run = True
        self.counter = 0
        self.counterLock = threading.Lock()
        self._dictLock = threading.Lock()
        self._retDict = {}
        self._eventDict = {}
        
    def scheduleTask(self, callbackFunc, args=[], kwargs={}, priority=NORMAL):
        ''' Starts the service that adds the tasks to the asynchronous scheduler queue.
        
        :param callbackFunc: A method that will be called when the task is finished.
        :param args: Optional. A list of arguments for the task.
        :param kwargs: Optional. A dicitionary of arguments for the task. 
        :param priority: Optional. The priority of the tasks.
        :raise SchedulerStoppedException: Raised if the service is stopped. 
        
        '''
        self._addTask(priority, callbackFunc, args, kwargs)
        
    def scheduleSyncTask(self, callbackFunc, args=[], kwargs={}, priority=NORMAL):
        ''' Starts the service that adds the tasks to the synchronous scheduler queue.
        
        :param callbackFunc: A method that will be called when the task is finished.
        :param args: Optional. A list of arguments for the task.
        :param kwargs: Optional. A dictionary of arguments for the task.
        :param priority: Optional. The priority of the tasks.
        :raise SchedulerStoppedException: Raised when the service stops or is stopped. 
        
        '''
        return self._addTask(priority, callbackFunc, args, kwargs, True)
        
    def _addTask(self, priority, callbackFunc, args, kwargs, syncTask=False, repeated=False):
        ''' This method implements the logic for the methods scheduleTask and scheduleSyncTask.'''
        with self.counterLock:
            try:
                self.tasks.put_nowait((priority, self.counter, callbackFunc, args, kwargs, syncTask, repeated))
            except queue.Full:
                raise SchedulerFullException("Reached for number of schedulable tasks")
            ctRef = self.counter
            self.counter += 1
        if syncTask:
            
            readyEvent = threading.Event()
            
            with self._dictLock:
                if not self.run:
                    raise SchedulerStoppedException("Scheduler has stopped.")
                self._eventDict[ctRef] = readyEvent
            
            readyEvent.wait()
            
            if not self.run:
                raise SchedulerStoppedException("Scheduler has stopped. A response may have been discarded")
            
            with self._dictLock:
                if ctRef not in self._retDict:
                    raise SchedulerException("Invalid state. Scheduler does not have a response!")
                self._eventDict.pop(ctRef)
                resp = self._retDict.pop(ctRef)
            
            if isinstance(resp, Exception):
                raise resp
            return resp
        
    def addRepeatedTask(self, priority, interval, callbackFunc, args, kwargs):
        ''' Adds the tasks and schedules them to be repeated in interval times. 
        
        :param interval: The time interval between task executions. 
        :param callbackFunc: A method that will be called everytime the task finishes.
        :param args: Optional. A list of arguments for the task.
        :param kwargs: Optional. A dictionary of arguments for the task. 
        :param priority: Optional. The priority of the tasks.
        
        '''
        if callbackFunc.__name__ in self.repeatedTasks:
            raise SchedulerException("{} has allready been scheduled as a repeated task".format(callbackFunc.__name__))
        self.repeatedTasks.append((priority, interval, callbackFunc, args, kwargs))
        self.repeatedTaskLastExe[callbackFunc.__name__] = datetime.datetime.now()

    def runScheduler(self, limmit=None):
        ''' Starts the  Scheduler service.
        
        :param limmit: Optional. Sets the limit time in seconds the service will run. 
        
        '''
        logger.debug("scheduler started. Thread {}".format(threading.get_ident()))
        stTs = datetime.datetime.now()
        try:
            while self.run:
                nowTs = datetime.datetime.now()
                if limmit and (nowTs - stTs).total_seconds() > limmit:
                    self.run = False
                    break
                for priority, interval, callbackFunc, args, kwargs in self.repeatedTasks:
                    if (nowTs - self.repeatedTaskLastExe[callbackFunc.__name__]).total_seconds() > interval:
                        self._addTask(priority, callbackFunc, args, kwargs, False, True)
                try:
                    _, tskCounter, callbackFunc, args, kwargs, isSync, isRepeatedTask = self.tasks.get(block=False)
                    if isRepeatedTask:
                        self.repeatedTaskLastExe[callbackFunc.__name__] = datetime.datetime.now()
                    try:
                        retVal = callbackFunc(*args, **kwargs)
                    except Exception as e:
                        logger.exception("Callback {} raised an exception in scheduler. For async tasks this exception ends here".format(str(callbackFunc)))
                        retVal = e
                    if isSync:
                        with self._dictLock:
                            self._retDict[tskCounter] = retVal
                            self._eventDict[tskCounter].set()
                except queue.Empty:
                    time.sleep(0.005)
            with self._dictLock:
                for tskCounter in self._eventDict:
                    self._eventDict[tskCounter].set()
        except Exception:
            logger.exception("Scheduler exited due to exception. Thread {}".format(threading.get_ident()))
            raise
        else:
            logger.debug("Scheduler exited. Thread {}".format(threading.get_ident()))
        
    def stop(self):
        ''' Stops the  Scheduler service '''
        logger.debug("Scheduler stopped")
        self.run = False
