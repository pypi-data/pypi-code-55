'''
Created on 14 Aug 2019

@author: joachim
'''

import subprocess
import logging

from threading import Thread, Lock
from uuid import uuid4
import signal

logger = logging.getLogger(__name__)

def preexec_function():
    # Ignore the SIGINT signal by setting the handler to the standard
    # signal handler SIG_IGN.
    signal.signal(signal.SIGINT, signal.SIG_IGN)

class ProcessController:
    
    def __init__(self):
        self.runningAsyncProcesses = {}
        self.runningAsyncProcessesLock = Lock()
        #self.threadLimmit = threadLimmit
    
    def run_cmd(self, cmdList, raiseErrorOnNonZeroExit=True, ignoreSigint=False):
        logger.debug("About to run command via system call '{}'".format(cmdList))
        kwargs = {}
        if ignoreSigint:
            kwargs["preexec_fn"] = preexec_function
        result = subprocess.run(cmdList, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
        stdOut = result.stdout
        stdErr = result.stderr
        if result.returncode == 0:
            logger.debug("Command exited with exit code 0")
            logger.debug("Stdout: " + str(stdOut))
            logger.debug("Stderr: " + str(stdErr))
        else:
            logger.warn("Command '{}' exited with exit code {}".format(cmdList, result.returncode))
            logger.info("Stdout: "+ str(stdOut))
            logger.info("Stderr: "+str(stdErr))
        if raiseErrorOnNonZeroExit:
            result.check_returncode()
        return result.returncode, stdOut, stdErr
    
    def _run_cmd_async_target(self, cmdList, okCallback, errorCallback, exitCallback, threadId, ignoreSigint=False):
        try:
            retCode, stdOut, stdErr = self.run_cmd(cmdList, raiseErrorOnNonZeroExit=False, ignoreSigint=ignoreSigint)
            if retCode == 0:
                if okCallback != None:
                    okCallback(retCode, stdOut, stdErr)
            else:
                if errorCallback != None:
                    errorCallback(retCode, stdOut, stdErr)
            if exitCallback:
                exitCallback(retCode, stdOut, stdErr)
        finally:
            with self.runningAsyncProcessesLock:
                self.runningAsyncProcesses.pop(threadId)
                
    
    def run_cmd_async(self, cmdList, okCallback=None, errorCallback=None, exitCallback=None, ignoreSigint=False):
        threadId = uuid4()
        with self.runningAsyncProcessesLock:
            while threadId in self.runningAsyncProcesses:
                threadId = uuid4()
        t = Thread(target=self._run_cmd_async_target, name="Process_thread_{}".format(cmdList[0]), args=[cmdList, okCallback, errorCallback, exitCallback, threadId, ignoreSigint])
        with self.runningAsyncProcessesLock:
            self.runningAsyncProcesses[threadId] = t
        t.start()
        
#     
#     def run_application_async(self, applicationId, applicationArgumentList, okCallback=None, errorCallback=None, exitCallback=None):
#         self.run_cmd_async(self._get_application_cmd(applicationId, applicationArgumentList), okCallback, errorCallback, exitCallback)
#     
#     def run_application(self, applicationId, applicationArgumentList, raiseErrorOnNonZeroExit=True):
#         return self.run_cmd(self._get_application_cmd(applicationId, applicationArgumentList), raiseErrorOnNonZeroExit)
    
    