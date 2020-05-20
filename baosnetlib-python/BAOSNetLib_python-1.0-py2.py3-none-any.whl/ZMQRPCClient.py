import zmq
import json
import threading
from threading import Lock

class ZMQRPCClient(object):
    def __init__(self):
        self.m_context = zmq.Context()
        #  Socket to talk to server
        self.m_socket = self.m_context.socket(zmq.REQ)
        self.m_lock = Lock()
    
    def connect(self,endpoint):
        self.m_socket.connect(endpoint)
    
    def make_json_request(self,id,method,params = None):
        json_dict = {
		"jsonrpc" : "2.0",
		"method": method,
		"id": id
        }

        if(params != None):
            json_dict["params"] = params

        json_str = json.dumps(json_dict)
        json_bytes = bytes(json_str, encoding = "utf8")
        return json_bytes

    # string method , json params , return json
    def call(self, method, params =None):
        data = self.make_json_request(1,method,params)

        self.m_lock.acquire()
        self.m_socket.send(data)

        reply = self.m_socket.recv()
        self.m_lock.release()
        # change bytes to json and return
        # print("client recv data is ",reply)
        json_str = str(reply, encoding = "utf-8")  
        result = json.loads(json_str)
        # print("recieve json is : ",result)

        return result
    
    def async_call(self,method,params,callback):
        if(callable(callback) != True):
            print("callback must be function")
            return -1

        new_thread = threading.Thread(target=self.async_call_proc,args=(method,params,callback))
        new_thread.start()
    
    def async_call_proc(self,method,params,callback):
        result = self.call(method,params)
        callback(result)
