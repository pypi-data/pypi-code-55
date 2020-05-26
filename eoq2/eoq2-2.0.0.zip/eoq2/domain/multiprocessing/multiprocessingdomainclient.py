'''
 2019 Bjoern Annighoefer
'''

from .multiprocessingcallmanager import MutliprocessingQueueCallManager
from ..domain import Domain
from ...serialization import JsonSerializer
from ...command.result import ResTypes,Res
from ...frame import Frame,FrameTypes
from ...util.error import EoqError

import queue # imported for using queue.Empty exception


'''
 CLIENT
 
'''

class MultiprocessingQueueDomainClient(Domain):
    def __init__(self,cmdQueue,resQueue,serializer=JsonSerializer(),timeout=1000000):
        self.cmdQueue = cmdQueue
        self.resQueue = resQueue
        self.timeout = timeout
        self.serializer = serializer
        self.callManager = MutliprocessingQueueCallManager(cmdQueue,serializer)
        self.cmdId = 0
        
    def RawDo(self, cmd, sessionId=None):
        # TODO: fix sessionID
        currentCmdId = self.cmdId;
        self.cmdId += 1
        frame = Frame(FrameTypes.CMD,currentCmdId,cmd)
        framesStr = self.serializer.Ser([frame])
        self.cmdQueue.put(framesStr)
        try:
            resFramesStr = self.resQueue.get(timeout=self.timeout)
            resFrames = self.serializer.Des(resFramesStr)
            if(1 != len(resFrames) or resFrames[0].uid != currentCmdId):
                raise EoqError("MultiProcessingClientDomain: Received invalid response to cmd %d: len: %d, resId: %d"%(currentCmdId,len(resFrames),resFrames[0].uid))
            result = resFrames[0].dat
        except queue.Empty:
            result = Res(cmd.cmd,ResTypes.ERR,"Internal multiprocessing queue receive timeout after %s s."%(self.timout))
        
        return result
