'''
Created on 21 Nov 2019

@author: joachim
'''
import logging
from multiprocessing.connection import Listener, Connection, Client,\
    SocketListener
import threading
import socket
import os

from k3process import ipc
from k3process.rpc import rpc_common
import time
from k3process.rpc.rpc_common import K3RPCSessionProvider, K3RPCClientServerSession
from threading import Thread

logger = logging.getLogger(__name__)

ACCEPT_RETURN = "KJVSHRPANV_server_exit"

class _CustomSocket:
    def __init__(self, address, backlog=1):
        family="AF_INET"
        self._socket = socket.socket(socket.AF_INET)
        try:
            # SO_REUSEADDR has different semantics on Windows (issue #2550).
            if os.name == 'posix':
                self._socket.setsockopt(socket.SOL_SOCKET,
                                        socket.SO_REUSEADDR, 1)
            self._socket.setblocking(True)
            self._socket.bind(address)
            self._socket.listen(backlog)
            self._address = self._socket.getsockname()
        except OSError:
            self._socket.close()
            raise
        self._family = family
        self._last_accepted = None
            
    def get_connection(self):
        s, self._last_accepted = self._socket.accept()
        s.setblocking(True)
        return Connection(s.detach())
    
    def get_local_address(self):
        return self._address
    
    def close(self):
        self._socket.close()
    
class K3RPCServerClientConnection:
    
    def __init__(self, remoteAddress, connection, sessionProvider = None):
        self.clientId = None
        self.connection = connection
        self.remoteAddress = remoteAddress
        self.sessionProvider = sessionProvider
        self.ipcCon = None
        self.conThread = Thread(target=self._run)
        self.readyNotifyThread = threading.Thread(target=self._ready_notify_run)
        self.readyEvent = threading.Event()
        
        
    def start_servering_connection_w_internal_thread(self):
        self.conThread.start()
        
    def _ready_notify_run(self):
        self.readyEvent.wait(1)
        self.ipcCon.waitForRemoteReady(1)
        logger.debug(f"Remote client {self.clientId} is ready")
        if self.clientSess:
            self.clientSess.client_ready(self.ipcCon)
        self.ipcCon.notifyReady()

    def _run(self):
        logger.info("Running connection thread for connection from ".format(self.remoteAddress))
        
        clientId = self.connection.recv()
        
        if clientId == ACCEPT_RETURN:
            self.connection.close()
            return
        
        self.readyNotifyThread.start()
        
        logger.info("Client ID of connector is {}".format(clientId))
        self.clientId = clientId
        
        self.clientSess = self.sessionProvider.new_incomming_rpc_connection(self.remoteAddress, self.clientId) if self.sessionProvider else None
        
        scheduler = self.clientSess.get_scheduler() if self.clientSess else None
        self.ipcCon = ipc.IPCConnection("server_"+self.clientId, scheduler=scheduler)
        
        self.ipcCon.setReceiveSendCallables(self.connection.recv, self.connection.send)
        if self.clientSess:
            self.ipcCon.registerTargetModule(self.clientSess.get_rpc_target(self.ipcCon))
        logging.info("Starting new client ({}) session.".format(self.clientId))
        try:
            self.ipcCon.runIPC(self.readyEvent)
            logger.info("IPC for {} done".format(self.clientId))
        except Exception:
            logger.warning("IPC for {} exited with exception", exc_info=True)
        finally:
            if self.clientSess:
                self.clientSess.session_ended()
            pass
        logger.info("IPC for {} done".format(self.clientId))
    
    def stop(self):
        if self.ipcCon:
            self.ipcCon.stopIPCConnection()
    
    def get_session_api(self):
        self.readyEvent.wait(1)
        self.ipcCon.waitForRemoteReady(1)
        return  K3RPCClientServerSession(self.clientId, self.remoteAddress, self.ipcCon)
    
    def __enter__(self):
        return self.get_session_api()
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
        return False
    
class K3RPCServer:
    
    def __init__(self, port, authenticationString, notUsedCompatibilityArg=None):
        self.port = port
        self.authenticationString = authenticationString
        self.socketListner = None
        
#     def accept_thread(self):
#         logger.debug("Initialising K3RPCServerClientConnection obj + thread")
    
    def accept(self, k3sessionProvider : K3RPCSessionProvider =None):
        if not self.socketListner:
            raise rpc_common.K3RPCException("K3RPCServer cannot accept connections as it has not bound a port yet. Use bind or a context manager.")
        init_conn = self.socketListner.accept()
        
        clientHost = self.socketListner.last_accepted[0]
        clientPort = self.socketListner.last_accepted[1]
        
        clientAddress = (clientHost, clientPort)
        
        logger.info('Connection accepted from client addr {}:{}'.format(clientHost, clientPort))
        
        clientSess = K3RPCServerClientConnection( clientAddress, init_conn, k3sessionProvider)
        clientSess.start_servering_connection_w_internal_thread()
        return clientSess
            
    
    def get_bound_port(self):
        return self.port
    
    def bind_address(self):
        self.socketListner = Listener(("0.0.0.0", self.port), authkey=self.authenticationString)
    
    def stop(self):
        self.socketListner.close()
    
    def __enter__(self):
        self.bind_address()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
        return False


class K3RPCSessionServer:
    
    def __init__(self, port, authenticationString, clientSrvPortRangeStart):
        self.runServer = True
        self.clientConnections = []
        self.clientConnectionsLock = threading.Lock()
        self.port = port
        self.authenticationString = authenticationString
        self.clientSrvPortRangeStart = clientSrvPortRangeStart
        self.running = False
        
    def _client_thread(self, serverClientConnection : K3RPCServerClientConnection):
        with serverClientConnection as rpcSessionAPI:
            logger.info("New session received from client {} at address {}".format(rpcSessionAPI.remote_id(), rpcSessionAPI.remote_address()))
            with self.clientConnectionsLock:
                self.clientConnections.append(serverClientConnection)
                logger.info("Number of clients connected: {}".format(len(self.clientConnections)))
            rpcSessionAPI.wait_remote_close()
            with self.clientConnectionsLock:
                self.clientConnections.remove(serverClientConnection)
            logger.info("Session from client {} at address {} done".format(rpcSessionAPI.remote_id(), rpcSessionAPI.remote_address()))
        
        
    def run(self, remoteRpcSessionProvider : K3RPCSessionProvider):
        with K3RPCServer(self.port, self.authenticationString, self.clientSrvPortRangeStart) as rpcServer:
            self.running = True
            while self.runServer:
                rpcConnection = rpcServer.accept(remoteRpcSessionProvider)
                if not self.runServer: # accept returns a none if accept is interrupted
                    if rpcConnection != None:
                        rpcConnection.stop()
                    continue
                Thread(target=self._client_thread, args=[rpcConnection]).start()
            logger.debug("Server loop exited")
        self.running = False
        logger.debug("Server run method exited")
        
            
    def stop(self):
        logger.debug("Run server set to false")
        with self.clientConnectionsLock:
            self.runServer = False
            for clientCon in self.clientConnections:
                clientCon.stop()
            if self.running:
                with Client(("0.0.0.0", self.port), authkey=self.authenticationString) as client:
                    client.send(ACCEPT_RETURN)
                    pass
        logger.info("Server close notification done")
