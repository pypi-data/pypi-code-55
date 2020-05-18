"""
Server side proxy api and implementation
"""

import logging
from threading import Thread, Event
from k3process import scheduler, rpc
import time
import json
import threading
logger = logging.getLogger(__name__)

class _Target:
    
    def __init__(self, clientPorxyTarget):
        self.clientPorxyTarget = clientPorxyTarget
        self.fixedReturnDict = {}
        self.dictLock = threading.Lock()
        
    def proxy_stub_call(self, functionName, kwargs):
        logger.debug(f"received proxy_stub_call '{functionName}' '{kwargs}'")
        with self.dictLock:
            if functionName in self.fixedReturnDict:
                return self.fixedReturnDict[functionName]
        return getattr(self.clientPorxyTarget, functionName)(**kwargs)
    
    def set_fixed_return(self, functionName, returnValue):
        with self.dictLock:
            logger.info("For function '{}' setting fixed return: {}".format(functionName, returnValue))
            self.fixedReturnDict[functionName] = returnValue
        
    def clear_fixed_return(self, functionName):
        with self.dictLock:
            logger.info("For function '{}' clearing fixed return".format(functionName))
            self.fixedReturnDict.pop(functionName)

class ProxyServer:
    
    def __init__(self, proxyConfigPath, clientPorxyTarget):
        with open(proxyConfigPath) as fp:
            conf = json.load(fp)
            self.port = conf["port"]
            self.authenticationString = bytes(conf["auth_key"], 'utf-8')
            self.stubDefinitionFile = conf["stub_function_definition"]
        self.recvThread = Thread(target=self._run, name="stub_server_proxy_recv")
        self.target = _Target(clientPorxyTarget)
        self.proxyStopped = False
        self.proxyRunningEvent = Event()

    def _run(self):
        s = scheduler.Scheduler(200)
        Thread(target=s.runScheduler, name="prx_server_recv_scheduler").start()
        logger.debug("Scheduler started")
        try:
            
            with rpc.K3RPCServer(self.port, self.authenticationString) as server:
                self.server = server
                logger.info(f"Server is running on bound port {self.port}")
                with server.accept() as rpcClientSession:
                    logger.info("Client part of proxy connected.")
                    rpcClientSession.set_target(self.target)
                    self.proxyRunningEvent.set()
                    logger.info("Clinet proxy target set. Waiting till stop_proxy_server is called")
                    while not self.proxyStopped:
                        time.sleep(0.01)
                    logger.info("ProxyServer initating close")
        except Exception as e:
            logger.error("Proxy server receive thread raised an exception", exc_info=True)
        finally:
            logger.info("Proxy server receive thread done")
            s.stop()
            
    def set_fixed_return(self, functionName, returnValue):
        self.target.set_fixed_return(functionName, returnValue)
    
    def clear_fixed_return(self, functionName):
        self.target.clear_fixed_return(functionName)

    def start_proxy_server(self):
        logger.info("start_proxy_server has been called")
        self.recvThread.start()

    def wait_till_client_connected(self, timeout):
        if not self.proxyRunningEvent.wait(timeout):
            raise TimeoutError("wait_till_client_connected timed out")
        
    def stop_proxy_server(self):
        logger.info("stop_proxy_server has been called")
        self.proxyStopped = True
        self.server.stop()



def init_proxy_server(proxyConfigPath, clientPorxyTarget)->ProxyServer:
    return ProxyServer(proxyConfigPath, clientPorxyTarget)
