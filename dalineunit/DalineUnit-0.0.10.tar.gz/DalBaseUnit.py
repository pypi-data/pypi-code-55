import re
import time
import json
import inspect
import threading
from CodeTest.puwrapper_pb2_grpc import PURequestServicer
from CodeTest.puwrapper_pb2 import RequestRetMsg

class DALJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


class DalBaseUnit(PURequestServicer):

    inprocess = False
    dataIF = []
    threads = []
    dicMethod = {}

    def _start_frame(self):
        difIF = {}
        if self.inprocess == True:
            print('Already in routine, do not call this function twice!')
            return
        funcs = inspect.getmembers(self, predicate=inspect.ismethod)
        self.inprocess = True
        for (name, method) in funcs:
            self.dicMethod[name] = method
            matchObj = re.match('(.*)_Info',name)
            if matchObj is not None:
                difIF['fidx'] = matchObj.group(1)
                difIF['info'] = method()
                self.dataIF.append(difIF)
            if re.match('(.*)_NewData',name) is not None:
                p = threading.Thread(target=DalBaseUnit._run_new_data,args=(self,method))
                p.start()
                self.threads.append(p)
    
    def _run_new_data(self,fun_new_data):
        while self.inprocess:
            fun_new_data()
            time.sleep(0.01)    

    def logError(self,content):
        return

    def logWarn(self,content):
        return

    def logInfo(self,content):
        return

    def quit(self):
        self.inprocess = False
        for th in self.threads:
            th.join()
        
    def newdata(self,dicMeta,dicData):
        print('New data meta[{}], data[{}]'.format(dicMeta,dicData))

    def Request(self, request, context):
        retDic = {}
        funName = ''
        CT = True
        dictReq = json.loads(request.strReq)

        retDic['retCode'] = 0
        retDic['retInfo'] = 'Success'
        retDic['retContent'] = ''
        dictUser = dictReq['user']
        dictInput = dictReq['input'] 
        if dictInput['type'] == 'QuerySystem':
            retDic['retContent'] = json.dumps(self.dataIF)
            CT = False
        if CT and ('user' not in dictReq or 'input' not in dictReq):
            retDic['retCode'] = 1
            retDic['retInfo'] = 'Input parameter format wrong, user and input should be set!'
            CT = False         
        if CT and ('fidx' not in dictInput or 'type' not in dictInput):
            retDic['retCode'] = 1
            retDic['retInfo'] = 'Fidx or type not defined'
            CT = False 
        if CT:
            if dictInput['type'] == 'QueryMeta':
                funName = dictInput['fidx']+'_Meta'
            elif dictInput['type'] == 'QueryData':
                funName = dictInput['fidx']+'_Data'
            elif dictInput['type'] == 'SubMeta':
                #todo
                todo = 1
            elif dictInput['type'] == 'SubData': 
                #todo
                todo = 1
            else:
                retDic['retCode'] = 3
                retDic['retInfo'] = 'Operation type should be one of QueryMeta,QueryData,SubMeta,SubData'
                CT = False  
        if CT and (funName not in self.dicMethod):
            retDic['retCode'] = 4
            retDic['retInfo'] = 'Function {} not fount in this unit!'.format(funName)
            CT = False            
        if CT:
            retDic = self.dicMethod[funName](dictUser,dictInput)
        ret = RequestRetMsg(strRet=json.dumps(retDic,cls=DALJsonEncoder))
        return ret