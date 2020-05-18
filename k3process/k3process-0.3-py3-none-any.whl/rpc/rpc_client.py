'''
Created on 22 Nov 2019

@author: joachim
'''
import logging
import socket
import os
import threading
from multiprocessing.connection import Client, Connection

from k3process import ipc
from k3process.rpc import rpc_common

logger = logging.getLogger(__name__)

def _getClientSocket(address):
    family = 'AF_INET'
    with socket.socket( getattr(socket, family) ) as s:
        s.setblocking(True)
        s.connect(address)
        return Connection(s.detach())

class K3RPCClinetConnection(rpc_common.K3RPCClientServerSession):
    
    def __init__(self, clientId, serverHost, serverPort, authKey, scheduler=None):
        self.clientId = clientId
        self.serverHost = serverHost
        self.serverPort = serverPort
        self.authKey = authKey
        self.scheduler = scheduler
        
        conToSrv = Client((self.serverHost, self.serverPort), authkey=self.authKey)
        logger.info("Contact to {} established".format((self.serverHost, self.serverPort)))
        
        conToSrv.send(self.clientId)

        readyEvent = threading.Event()
        self.ipcCon = ipc.IPCConnection(self.clientId, scheduler=self.scheduler)
        self.ipcCon.setReceiveSendCallables(conToSrv.recv, conToSrv.send)
        self.ipcRecvThread = threading.Thread(target=self._ipc_recv_thread, args=(readyEvent,))
        self.ipcRecvThread.start()
        if not readyEvent.wait(timeout=2):
            self.ipcCon.stopIPCConnection()
            raise rpc_common.K3RPCException("Unable to establish connection to remote server within 2s timeout")
        else:
            self.ipcCon.notifyReady()
        
        self.ipcCon.waitForRemoteReady(1)
        logger.info("Server ({}) IPC connection ready.".format((self.serverHost, self.serverPort)))
        super().__init__(clientId, (self.serverHost, self.serverPort), self.ipcCon)
            
    def _ipc_recv_thread(self, readyEvent):
        logger.debug("IPC receive thread started")
        self.ipcCon.runIPC(readyEvent)
        logger.debug("IPC receive thread completed")
    
    def _disconnect(self):
#         with self.intiLock:
#             if not self.initalised:
#                 return
        self.ipcCon.stopIPCConnection()

class K3RPCClient:
    
    def __init__(self, clientId, host, port, authKey, clientTarget=None, scheduler=None):
        self.clientId = clientId
        self.host = host
        self.port = port
        self.authKey = authKey
        self.clientTarget = clientTarget
        self.scheduler = scheduler
        self.currentConnection = None
        
    def connect(self):
        if self.currentConnection != None:
            raise rpc_common.K3RPCException("An connection to server by rpc client {} has already been established".format(self.clientId))
        self.currentConnection = K3RPCClinetConnection(self.clientId, self.host, self.port, self.authKey, scheduler=self.scheduler)
        if self.clientTarget != None:
            self.currentConnection.set_target(self.clientTarget)
        return self.currentConnection
    
    def disconnect(self):
        self.currentConnection._disconnect()
        self.currentConnection = None
    
    def __enter__(self):
        self.connect()
        return self.currentConnection
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.currentConnection != None:
            self.disconnect()
        else:
            logger.warning("Cannot close connection. RPC connection for client {} was already closed".format(self.clientId))
        return False
    
