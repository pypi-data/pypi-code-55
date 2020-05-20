import json
import zmq
import threading
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
import time
from Baos.multicast import *
from Baos.ZMQRPCServer import *
from Baos.ZMQRPCClient import *

import asyncio
import socket

# socket info
class socketInfo(object):
    def __init__(self,socket,flag):
        self.socket = socket
        self.flag = flag

# auto auto lock class 
# input a lock and start lock when init
# When out of scope, the destructor is called to release the lock
class AutoLock:
    def __init__(self,lock):
        self._lock = lock
        self._lock.acquire()

    def __del__(self):
        self._lock.release()

class BaosNodeImpl(object):
    m_instance = None
    m_poolSize = 10

    def __init__(self):
        self.m_mutex = []
        self.m_index = 0
        for i in range(BaosNodeImpl.m_poolSize):
            self.m_mutex.append(Lock())
        self.m_connManager = None
        self.m_pool = None
        self.m_servers = None
        self.m_workers = None
        self.m_context = None
        self.m_callback = {"sub":None}
        self.m_jsonHandlers = {}    #{string,[jscb]}
        self.m_msgHandlers = {}     #{string,[msgcb]}
        self.m_msgQueue = [i for i in range(BaosNodeImpl.m_poolSize)]    # message queue to save recieve
        self.m_connection = {}
        self.m_connectionDealWay = {}   # {string,[int]}
        self.m_connectionJson = {}  # {string,socket}

        self.m_localIP = None
        self.m_pubsubPort = None
        self.m_rpcPort = None


        self.m_poller = zmq.Poller() 
        self.m_socketInsVec = [] # [{flag,socket}]
        self.m_websocket = None

        pass
    
    def initialize(self, multiIP, point = None):
        self.m_connManager = Multicast(multiIP,self.m_localIP)
        self.m_localIP = self.m_connManager.get_localip()
        print("self.m_localIP is ",self.m_localIP)
        
        # get free port
        self.m_rpcPort = str(self.get_free_port())
        self.m_pubsubPort = str(self.get_free_port())

        # pub&sub init
        self.m_topicEndpoint = "tcp://" + self.m_localIP + ":" + self.m_pubsubPort
        print("ZMQ PUB Binding to ",self.m_topicEndpoint)
        self.m_context = zmq.Context()
        self.m_pub = self.m_context.socket(zmq.PUB)
        self.m_pub.bind(self.m_topicEndpoint)

        # zmq rpc server init
        self.m_serviceEndpoint =  "tcp://" + self.m_localIP + ":"  + self.m_rpcPort
        ZMQRPCServer.getInstance().initServer(self.m_serviceEndpoint, BaosNodeImpl.m_poolSize)

        self.m_rpcConnection = {}

        # multicast run and basnodeimpl's dealpoller run
        self.m_connManager.setLocalEndpoint(self.m_topicEndpoint, self.m_serviceEndpoint)
        self.m_pool = ThreadPoolExecutor(max_workers=BaosNodeImpl.m_poolSize)   # init thread pool size
        self.m_pool.submit(Multicast.run, self.m_connManager)
        self.m_pool.submit(self.dealpoller)
    
    def init(self):
        self.initialize(g_multicast_addr,None)

    @classmethod
    def getInstance(cls):
        if(cls.m_instance == None):
            lock = Lock()
            lock.acquire()
            if(cls.m_instance == None):
                cls.m_instance = BaosNodeImpl()
            lock.release()
        return cls.m_instance
    
    # create protobuf message
    def createMessage(self,type_name):
        pass

    def runService(self):
        self.m_pool.submit(ZMQRPCServer.run,ZMQRPCServer.getInstance())

    # jsonrpcpp::request_callback f
    def registerService(self,serviceName, f):
        # multicast service
        self.m_connManager.multicastService(serviceName,"tcp://" + str(self.m_localIP) + ":" +  self.m_rpcPort)
        # register call
        ZMQRPCServer.getInstance().registerCall(serviceName, f)

    def callService(self,serviceName, params = None , callback = None):
        endpoints = []
        result = {}
        # if can not find service ,then update 
        if(self.m_connManager.findService(serviceName,endpoints) == False):
            servicecall = ServiceCall()
            servicecall.params = params
            servicecall.callback = callback
            servicecall.servCall = self.callService
            servicecall.serviceName = serviceName
            self.m_connManager.pushServiceCallBack(servicecall)
            self.m_connManager.sendRequest(serviceName, "service")
            return result
        
        # find serve and it's process it's related endpoints
        for endpoint in endpoints:
            # print("service endpoint is ",endpoint)
            # if alread found rpc connection in m_rpcConnection
            if(endpoint in self.m_rpcConnection.keys()):
                if(callback == None):
                    result = self.m_rpcConnection[endpoint].call(serviceName, params)
                else:
                    self.m_rpcConnection[endpoint].async_call(serviceName,params,callback)
            # if not found rpc connection in m_rpcConnection ,then create connection and save it
            else:
                self.m_rpcConnection[endpoint] = ZMQRPCClient()
                self.m_rpcConnection[endpoint].connect(endpoint)
                if(callback == None):
                    result = self.m_rpcConnection[endpoint].call(serviceName, params)
                else:
                    self.m_rpcConnection[endpoint].async_call(serviceName,params,callback)
            return result
        
        
    def publishTopic(self,topic):
        print("topic is ",topic,"  m_topicEndpoint is ",self.m_topicEndpoint)
        self.m_connManager.multicastTopic(topic, self.m_topicEndpoint)
    
    def publish_json(self,topic,json_str):
        sendstr = topic + '-' + str(json_str)
        sendbyte = bytes(sendstr,encoding="ISO-8859-1")
        self.m_pub.send(sendbyte)

        # Publish the data to each client that connects to the node via Websocket and fons to the topic
        pass

    def publish_msg(self,topic,msg):

        class_name = type(msg).__name__     # get object's class name
        msg = msg.SerializeToString()       # SerializeToString

        frame_start = topic + str('-"') 
        frame_end = class_name + str('*,')
        
        # format : topic_name + -classname* + msg
        sendbyte = bytes(frame_start,encoding="utf-8") + len(class_name).to_bytes(1,"big") \
            + bytes(frame_end,encoding="utf-8") + msg
        try:
            self.m_pub.send(sendbyte)
        except zmq.error as e:
            print("zmq publish protobuf msg error : ",e)
        
    def dealRecv(self, msg, flag , index):
        try:
            msg = str(msg,encoding="ISO-8859-1")
            auto_lock = AutoLock(self.m_mutex[self.m_index % BaosNodeImpl.m_poolSize])

            index = msg.find("-")
            topic = msg[0:index]
            content = msg[index+1:]

            if( flag == ProtoType ):
                index = content.find("*")     # find index of real protobuf msg except class name

                content = content[index+2:]     # get msg data
                param = bytes(content,encoding="ISO-8859-1")

                handlers = self.m_msgHandlers[topic]
                for handler in handlers:
                    handler(param)

            elif(flag == JsonType):
                param = json.loads(content)
                handlers = self.m_jsonHandlers[topic]   # handlers list for spectific topic
                for handler in handlers:
                    handler(param)
        except Exception as e:
            print("error is ",e)

    # add alread created and connect socket to list and add socket to zmq poller monitor
    def addSocket(self,socket, flag):
        self.m_poller.register(socket, zmq.POLLIN)
        self.m_socketInsVec.append(socketInfo(socket,flag))

    # zmq poller monitor socket and deal with socket recv
    def dealpoller(self):
        while(1):
            socks = self.m_poller.poll()    # socks [(socket,flag)]  
            # process poller monitor sockets
            for i in range(len(socks)):
                if(socks[i][1] == zmq.POLLIN):  #socket flag == zmq.POLLIN
                    try:
                        auto_lock = AutoLock(self.m_mutex[self.m_index % BaosNodeImpl.m_poolSize])
                        self.m_msgQueue[self.m_index % BaosNodeImpl.m_poolSize] = self.m_socketInsVec[i].socket.recv()

                    except zmq.error as e:
                        print(e)
                        continue
                    self.m_pool.submit(self.dealRecv, self.m_msgQueue[self.m_index % BaosNodeImpl.m_poolSize],
                                        self.m_socketInsVec[i].flag,self.m_index)
                    self.m_index = self.m_index + 1
                    if(self.m_index == BaosNodeImpl.m_poolSize):
                        self.m_index = 0
    
    # create new subcribe socket and add it into connection
    # use addSocket to put socket into poller monitor
    # insert endpoint into connectiondealway which use to check if endpoint is connect or not
    def initNewSub(self,endpoint, topic, flag):
        self.m_connection[endpoint] = self.m_context.socket(zmq.SUB)
        # print("initNewSub connect endpoint is ",endpoint)
        self.m_connection[endpoint].connect(endpoint)
        self.m_connection[endpoint].setsockopt_string(zmq.SUBSCRIBE,topic)

        self.addSocket(self.m_connection[endpoint],flag)

        if(topic not in self.m_connectionDealWay.keys()):
            vec = [0 for i in range(10)]
            self.m_connectionDealWay[endpoint] = vec
    
    def subscribeTopic_Json(self, topic, jsncb):
        endpoints = []
        endpoint = ""

        if( self.m_connManager.findTopic(topic, endpoints) == False ):
            # print("can not find topic")
            jsnCB = JsnCallBack()
            jsnCB.jsnCb = jsncb     # user json callback function
            jsnCB.jsnSub = self.subscribeTopic_Json         # baosnodeimpl.subscribeTopic_Json callback function
            jsnCB.topicName = topic

            self.m_connManager.pushTopic_JsonCallBack(jsnCB)
            self.m_connManager.sendRequest(topic,"topic")
            return

        print("subscribeTopic_Json find endpoints is ",endpoints)
        if(self.m_jsonHandlers.get(topic) == None):
            jsoncb_list = []
            jsoncb_list.append(jsncb)
            self.m_jsonHandlers[topic] = jsoncb_list
        else:
            self.m_jsonHandlers[topic].append(jsncb)

        for endpoint in endpoints:
            if(endpoint not in self.m_connectionJson.keys()):
                self.initNewSub(endpoint, topic, JsonType)
            else:
                self.m_connectionJson[endpoint].setsockopt_string(zmq.SUBSCRIBE, topic)
                if(self.m_connectionDealWay[endpoint][JsonType] == 0):
                    self.addSocket(self.m_connectionJson[endpoint], JsonType)
                    self.m_connectionDealWay[endpoint][JsonType] = 1

    def subscribeTopic_Msg(self, topic, msgcb):
        endpoints = []
        endpoint = ""

        if( self.m_connManager.findTopic(topic, endpoints) == False ):
            # print("can not find topic")
            msgCB = MsgCallBack()
            msgCB.msgCb = msgcb     # user json callback function
            msgCB.msgSub = self.subscribeTopic_Msg         # baosnodeimpl.subscribeTopic_Json callback function
            msgCB.topicName = topic

            self.m_connManager.pushTopic_MsgCallBack(msgCB)
            self.m_connManager.sendRequest(topic,"topic")
            return

        print("subscribeTopic_Msg find endpoints is ",endpoints)
        if(self.m_msgHandlers.get(topic) == None):
            msgcb_list = []
            msgcb_list.append(msgcb)
            self.m_msgHandlers[topic] = msgcb_list
        else:
            self.m_msgHandlers[topic].append(msgcb)

        for endpoint in endpoints:
            if(endpoint not in self.m_connection.keys()):
                self.initNewSub(endpoint, topic, ProtoType)
            else:
                self.m_connection[endpoint].setsockopt_string(zmq.SUBSCRIBE, topic)
                if(self.m_connectionDealWay[endpoint][ProtoType] == 0):
                    self.addSocket(self.m_connection[endpoint], ProtoType)
                    self.m_connectionDealWay[endpoint][ProtoType] = 1
    
    # get port automaticly allocated by os
    def get_free_port(self):  
        sock = socket.socket()
        sock.bind(('', 0))
        ip, port = sock.getsockname()
        sock.close()
        return port

    def unSubscribeTopic(self,topic):
        endpoints = []

        self.m_connManager.findTopic(topic,endpoints)

        # clear json data type connection and handlers
        for endpoint in endpoints:
            if( endpoint in self.m_connectionJson.keys() ):
                # cancel subscribe
                for i in range(len(self.m_jsonHandlers[topic])):
                    self.m_connectionJson[endpoint].setsockopt_string(zmq.UNSUBSCRIBE,topic)
                del self.m_jsonHandlers[topic]
                print("unsubscribe ",topic)

        # clear protobuf data type connection and handlers
            if(endpoint in self.m_connection.end()):
                for i in range(len(self.m_msgHandlers[topic])):
                    self.m_connection[endpoint].setsockopt_string(zmq.UNSUBSCRIBE,topic)
                del self.m_msgHandlers[topic]
                priint("unsubscribe ",topic)