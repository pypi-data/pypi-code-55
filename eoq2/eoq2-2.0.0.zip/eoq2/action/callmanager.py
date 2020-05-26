'''
 2019 Bjoern Annighoefer
'''

'''
 CALL MANAGER
'''

from .call import CallTypes,CallStatus,Call
from ..event import EvtProvider,CstEvt,CvaEvt,OupEvt
from ..util import EoqError

class CallManager(EvtProvider):
    def __init__(self,cmdRunner):
        super().__init__()
        self.cmdRunner = cmdRunner
        self.actionInfos = {} #'action name' -> (action,handler)
        self.currentCallId = 0 #only for async calls
        self.runningCalls = {} #callid -> (callback handler, abort handler, call status,)
    
    def RegisterAction(self,name,action,handler):
        self.actionInfos[name] = (action,handler)
        
    def UnregisterAction(self,name):
        self.actionInfos.pop(name)
        
    def GetAllActions(self):
        return [value[0] for value in self.actionInfos.values()]
       
    def ChangeCallStatus(self,callId,status):
        if((callId in self.runningCalls) and (self.runningCalls[callId].status != status)):
            self.runningCalls[callId].status = status
            self.NotifyObservers([CstEvt(callId,status)])
            
    def SetCallValue(self,callId,value):
        if(callId in self.runningCalls):
            self.runningCalls[callId].value = value
            self.NotifyObservers([CvaEvt(callId,value)],self)
            
    def AddCallOutput(self,callId,channelName,data):
        if(callId in self.runningCalls):
            callInfo = self.runningCalls[callId]
            if(channelName in callInfo.outputs):
                callInfo.outputs[channelName] += data
            else:
                callInfo.outputs[channelName] = data
            self.NotifyObservers([OupEvt(callId,channelName,data)],self)
            
    def RunCall(self,name,args,tid):
        #name = args[0]
        #obtain the handler
        info = self.actionInfos[name]
        action = info[0]
        handler = info[1]
        #check if the arguments are appropriate
        nActionArgs = len(args)
        nExpectedArgs = len(action.args)
        if(nActionArgs!=nExpectedArgs):
            raise EoqError(0,"Action %s requires %s arguments, but got %d."%(name,nExpectedArgs,nActionArgs))
        #call the handler
        callInfo = self.CreateNewCall(name, handler, CallTypes.SYN)
        domain = CallDomain(self.cmdRunner,tid) #create a private domain to be used within the action
        
        value = handler.HandleSync(name,callInfo.callId,domain,args,self)
        result = [callInfo.callId,value,callInfo.status,callInfo.outputs]
        return result
    
    def RunCallAsnyc(self,name,args,tid):
        info = self.actionInfos[name]
        action = info[0]
        handler = info[1]
        #check if the arguments are appropriate
        nActionArgs = len(args)
        nExpectedArgs = len(action.args)
        if(nActionArgs!=nExpectedArgs):
            raise EoqError(0,"Action %s requires %s arguments, but got %d."%(name,nExpectedArgs,nActionArgs))
        #call the handler
        callInfo = self.CreateNewCall(name, handler, CallTypes.SYN)
        domain = AsyncCallDomain(self.cmdRunner) #create a private domain to be used within the action
        
        handler.HandleAsync(name,callInfo.callId,domain,args,self)
        result = callInfo.callId
        return result
    
    
    def AbortCall(self,callId,tid):
        try:
            callInfo = self.runningCalls[callId]
            result = callInfo.handler.AbortCall(callId)
            if(result):
                self.ChangeCallStatus(callId, CallStatus.ABO)
        except KeyError:
            raise EoqError(0,"Call id %d is unknown."%(callId))
        return result
    
    '''
     PRIVATE METHODS
    '''
   
    def CreateNewCall(self,name,handler,ctype):
        callId = self.currentCallId
        self.currentCallId+=1
        callInfo = Call(callId,name,handler,ctype)
        self.runningCalls[callId] = callInfo
        return callInfo
    
'''
    A domain that wraps a specific transaction id
    Is used internally in the command runner for executing actions
'''   
        
from ..domain.domain import Domain
        
class CallDomain(Domain):
    def __init__(self,cmdRunner,tid):
        self.cmdRunner = cmdRunner
        self.tid = tid
       
    #@override 
    def RawDo(self,cmd,sessionId=None):
        # TODO: fix sessionId to do something
        res = self.cmdRunner.ExecOnTransaction(cmd,self.tid)
        return res
    
class AsyncCallDomain(Domain):
    def __init__(self,cmdRunner):
        self.cmdRunner = cmdRunner
       
    #@override 
    def RawDo(self,cmd):
        res = self.cmdRunner.Exec(cmd)
        return res
