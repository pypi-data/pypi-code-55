'''
 2019 Bjoern Annighoefer
'''

'''
    Server
'''

from ..domain import Domain
from ...serialization import JsonSerializer
from ...frame import FrameTypes
from ...event import EvtTypes

from multiprocessing import Queue
import queue # imported for using queue.Empty exception
   
import threading

class MultiprocessingQueueDomainHost(Domain):
    def __init__(self,domain,callManager,serializer=JsonSerializer(),timeout=0.1):
        self.domain = domain
        self.callManager = callManager
        self.cmdQueue = Queue()
        self.resQueue = Queue()
        self.timeout = timeout
        self.serializer = serializer
        self.shallRun = True
        
    def Start(self):
        self.listenerThread = threading.Thread(target=self.__RemoteCommandHandler, args=())
        self.listenerThread.start()
        
    def Join(self):
        self.shallRun = False
        self.listenerThread.join()
        
    def __RemoteCommandHandler(self):
        while self.shallRun:
            try:
                frameStr = self.cmdQueue.get(timeout=self.timeout)
                frames = self.serializer.Des(frameStr)
                outFrames = []
                for frame in frames:
                    if(frame.eoq==FrameTypes.CMD):
                        cmd = frame.dat
                        res = self.domain.RawDo(cmd)
                        frame.eoq = FrameTypes.RES
                        frame.dat = res
                        outFrames.append(frame)
                    elif(frame.eoq == FrameTypes.EVT):
                        evt = frame.dat
                        if(evt.evt == EvtTypes.OUP):
                            self.callManager.AddCallOutput(evt.a[0],evt.a[1],evt.a[2])
                        elif(evt.evt == EvtTypes.CST):
                            callId = evt.a[0]
                            status = evt.a[1]
                            self.callManager.ChangeCallStatus(callId,status)
                        elif(evt.evt == EvtTypes.CVA):
                            self.callManager.SetCallValue(evt.a[0],evt.a[1])
                #send a cumulative answer
                if(len(outFrames)>0):
                    frameStr = self.serializer.Ser(outFrames)
                    self.resQueue.put(frameStr) 
                    
            except queue.Empty:
                continue
            except:
                break