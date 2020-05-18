'''
This module contains the Inter Process Communication class implementation, 
responsible for the inter process communication:
• sharing an inter process channel for synchronous message exchange
• runs a dedicated thread for reception of messages
• calls a registered callback function on message reception
'''
import threading
import time

import logging

from tblib import pickling_support, Traceback
pickling_support.install()

from pickle import PicklingError
from threading import Event
import datetime

import pickle, sys

logger = logging.getLogger(__name__)


class _IPCRemoteException:
    def __init__(self, sysExecTuple):
        et, ev, tb = sysExecTuple
        tb = Traceback(tb)
        self.exceptionType = str(et)
        self.msg = str(ev)
        try:
            self.serialisedSysExecTuple = pickle.dumps((et,ev,tb))
        except PicklingError:
            ne = IPCRemoteExecutionException("Unable to transfer remote exception. Exceptions of type: {}. Message was: {}".format(et, str(ev)))
            self.serialisedSysExecTuple = pickle.dumps((type(ne), ne,tb))
        
    def getRemoteSysExecTuple(self):
        et, ev, tb = pickle.loads(self.serialisedSysExecTuple)
        return et, ev, tb.as_traceback()

class IPCException(Exception):
    pass

class IPCStoppedException(IPCException):
    pass

class IPCRemoteExecutionException(IPCException):
    pass

class IPCConnection:
    '''
    Inter Process Communication class responsible for the inter process communication:
    • sharing an inter process channel for synchronous message exchange
    • runs a dedicated thread for reception of messages
    • calls a registered callback function on message reception
    '''
    
    def __init__(self, ipcId, printDataFullInDebug=False, scheduler=None):
        ''' Initialization of the IPC connection.
        
        :param ipcId: The ID for the IPC.
        :param receivePipe: The pipe for the reception of messages.
        :param sendPipe: The pipe for sending messages.
        :param printDataFullInDebug: print complete contents of data to debug logging
        :param scheduler: an object which has scheduleSyncTask method that takes callback,
                          args, kwargs arguments and blocks until a result is received  
        '''
        self._ipcId = ipcId
        self.printDataFullInDebug = printDataFullInDebug
        self._recvFunc = None
        self._sendFunc = None
        self._targetModule = None
        self._respDict = {}
        self._eventDict = {}
        self._dictLock = threading.Lock()
        self._pipeLock = threading.Lock()
        self._tagLock = threading.Lock()
        self._tagCounter = 0
        self._remoteReady = False
        self.scheduler = scheduler
        self.run = True
        logger.debug("Debug messaging enabled for ipc")
        
    def _formatDebugData(self, data):
        if self.printDataFullInDebug:
            return data
        else:
            dataStr = str(data)
            return dataStr[:50] + " ... ({})".format(len(dataStr))
        
    def _send(self, data):
        ''' Sends the data through the sendPipe '''
        if self._sendFunc == None:
            raise IPCException("Cannot send data as setReceiveSendCallables have not been set")
        with self._pipeLock:
            logger.debug("{} IPC --> {}".format(self._ipcId, self._formatDebugData(data)))
            self._sendFunc(data)
    
    def _recv(self):
        ''' Receives a message through the receivePipe '''
        logger.debug("{} IPC waiting for message".format(self._ipcId))
        r = self._recvFunc()
        logger.debug("{} IPC <-- {}".format(self._ipcId, self._formatDebugData(r)))
        return r
    
    def registerTargetModule(self, targetModule):
        ''' Registers the target module.
        
        :param targetModule: The target module. 
        
        '''
        if self._targetModule:
            raise IPCException("A target module has already been registered")
        self._targetModule = targetModule
    
    def _call(self, functionNm, data, timeout=None):
        ''' Makes a function call through the sendPipe to the remote process.
        
        :param functionNm: The name of the function to be called.
        :param data: The args for the function.
        :return: The response received from the remote process. 
        
        '''
        logger.debug("{} IPC method {} was called with args: {}".format(self._ipcId, functionNm, self._formatDebugData((data))))
        with self._tagLock:
            tag = str(self._tagCounter)
            self._tagCounter += 1
            
        readyEvent = Event()
        
        with self._dictLock:
            if not self.run:
                raise IPCStoppedException("IPC has stopped.")
            self._eventDict[tag] = readyEvent
            
        self._send((tag, "req", functionNm, data))
        
        readyEvent.wait(timeout)
        
        if not self.run:
            raise IPCStoppedException("IPC has stopped. A recieved message may have been discarded")
        
        with self._dictLock:
            if tag not in self._respDict:
                if functionNm == "remoteStopIPCConnection":
                    logger.info("No response to remoteStopIPCConnection")
                    return None
                raise IPCException("Invalid state. IPC does not have a response!")
            self._eventDict.pop(tag)
            resp = self._respDict.pop(tag)
        
        if isinstance(resp, _IPCRemoteException):
            try:
                sysExeTuple = resp.getRemoteSysExecTuple()
            except Exception:
                logger.warning("Unable to interpret remote exception. Raising generic IPCRemoteExecutionException", exc_info=True)
                raise IPCRemoteExecutionException("Unable to transfer remote exception. Original exception type was: {}. Message was: {}".format(resp.exceptionType, resp.msg)) from None
            else:
                reraise(*sysExeTuple)
        return resp
            
    def setReceiveSendCallables(self, recv, send):
        '''Set the given recv and send callables.
        The send callable needs to be able to take an argument which is serialisable
        Function blocks thread till IPC has stopped
        '''
        self._recvFunc = recv
        self._sendFunc = send
        
    def runIPC(self, readyEvent=None):
        """  Run the icp. Blocks toll 
        
        """
        if not (self._recvFunc and self._sendFunc):
            raise IPCException("send/receive callable not set properly") 
        self._runReceiveThread(readyEvent)
        
    def _runReceiveThread(self, readyEvent):
        ''' Runs the loop for receiving messages. '''
        logger.info("{} IPC receive thread started".format(self._ipcId))
        if readyEvent != None:
            readyEvent.set()
        try:
            while self.run:
                tag, tp, functionNm, data = self._recv()
                if tp == "req":
                    if functionNm == "remoteStopIPCConnection":
                        self.run = False
                        self._send((tag, "res", functionNm, True))
                        continue
                    elif functionNm == "isRemoteTargetSet":
                        self._send((tag, "res", functionNm, (self._targetModule != None)))
                        continue
                    elif functionNm == "localIsReadyNow":
                        self._remoteReady = True
                        self._send((tag, "res", functionNm, "affirmative"))
                        continue
                    otherThread = threading.Thread(target=self._runRequestedFunc, args=(tag, functionNm, data))
                    otherThread.start()
                elif tp == "res":
                    with self._dictLock:
                        if functionNm == "remoteStopIPCConnection":
                            self.run = False
                        else:
                            self._respDict[tag] = data
                            self._eventDict[tag].set()
                else:
                    logger.warning("Unkown message type {}".format(tp))
        finally:
            with self._dictLock:
                for lTag in self._eventDict:
                    self._eventDict[lTag].set()
        logger.info("{} IPC receive thread stopped".format(self._ipcId))
    
    def _runRequestedFunc(self, tag, functionNm, data):
        ''' Runs the requested function and sends a response. '''
        try:
            if not self._targetModule:
                raise IPCException("IPC {} has no target set yet".format(self._ipcId))
            if self.scheduler:
                responeObj = self.scheduler.scheduleSyncTask(getattr(self._targetModule, functionNm),args=data)
            else:
                responeObj = getattr(self._targetModule, functionNm)(*data)
            self._send((tag, "res", functionNm, responeObj))
        except:
            logger.exception("remote call to {} function {} rasied an exception".format(self._ipcId, functionNm))
            self._send((tag, "res", functionNm, _IPCRemoteException(sys.exc_info())))
    
    def __getattr__(self, name):
        ''' Calls a method in the remote process and returns its response. 
        
        :param name: The method name to be called.
        :return: The response from the remote process. 
        :raise IPCStoppedException: Raised if the local process is not running. 
        
        '''
        def method(*args):
            if not self.run:
                raise IPCStoppedException("IPC has stopped")
            return self._call(name, args)
        return method
    
    def isRunning(self):
        return self.run
    
    def stopIPCConnection(self):
        ''' Stops the remote process. '''
        try:
            logger.debug("Stop IPC function called on IPC {}".format(self._ipcId))
            self._call("remoteStopIPCConnection", [], timeout=0.2)
            #self.remoteStopIPCConnection()
        except IPCStoppedException:
            pass
        finally:
            self.run = False
    
    def notifyReady(self):
        self.localIsReadyNow()
        
    def isRemoteReady(self):
        return self._remoteReady
    
    def waitForRemoteReady(self, timeout=None):
        if timeout is None:
            timeout = float("inf")
        startTime = datetime.datetime.now()
        while (datetime.datetime.now() - startTime).total_seconds() < timeout:
            if self.isRemoteReady():
                return
            if not self.isRunning():
                raise  IPCStoppedException("IPC has stopped")
            time.sleep(0.01)
        raise IPCException("Timout reached while waiting for remote to be ready")
        
        
    def waitForRemoteTargetSet(self, timeout=None):
        if timeout is None:
            timeout = float("inf")
        startTime = datetime.datetime.now()
        while (datetime.datetime.now() - startTime).total_seconds() < timeout:
            if self.isRemoteTargetSet():
                return
            if not self.isRunning():
                raise  IPCStoppedException("IPC has stopped")
            time.sleep(0.01)
        raise IPCException("Timeout reached while Waiting for remote target to be set")
        
#         
#     def _stopIPCConnectionForce(self):
#         try:
#             self._call("remoteStopIPCConnection", [], timeout=1)
#         except IPCException:
#             logger.warning("On force remoteStopIPCConnection timeout was reached or other error occurred", exc_info=True)
#             self.run = False
#         except IPCStoppedException:
#             pass

# PY 3 implemenation taken from six.reraise
def reraise(eType, value, tb=None):
    try:
        if value is None:
            value = eType()
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value
    finally:
        value = None
        tb = None
