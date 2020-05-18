'''
Created on 22 Nov 2019

@author: joachim
'''

from abc import abstractmethod, ABCMeta
from k3process import ipc
import time

class K3RPCException(Exception):
    pass

def client_init_finished_str(clientId):
    return "client_{}_ready".format(clientId)

class K3RPCClientServerSession(metaclass=ABCMeta):
    
    def __init__(self, remoteId, remoteAddress, ipc):
        self.ipc = ipc
        self.remoteAddress = remoteAddress
        self.remoteId = remoteId
    
    def set_target(self, targetModule):
        self.ipc.registerTargetModule(targetModule)

    def remote_id(self):
        return self.remoteId

    def remote_address(self):
        return self.remoteAddress
    
    def wait_remote_close(self):
        while True:
            if not self.ipc.isRunning():
                return
            time.sleep(0.01)

    def wait_remote_target_set(self, timeout=None):
        self.ipc.waitForRemoteTargetSet(timeout)

    def get_remote_target_proxy(self):
        return self.ipc

class K3RPCSession(metaclass=ABCMeta):
    
    @abstractmethod
    def get_rpc_target(self, ipcConnection : ipc.IPCConnection):
        return None
    
    def get_scheduler(self):
        return None
    
    def client_ready(self, ipcConnection : ipc.IPCConnection):
        pass
    
    def session_ended(self):
        pass

class K3RPCSessionProvider(metaclass=ABCMeta):
    
    @abstractmethod
    def new_incomming_rpc_connection(self, clientAddress, clientId) -> K3RPCSession:
        #return ipcTarget, scheduler, startupCallback, connectionEndCallback
        return None