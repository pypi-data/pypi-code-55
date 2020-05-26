'''
 2019 Bjoern Annighoefer
'''

class CallTypes:
    SYN = 'SYN'
    ASY = 'ASY'
    
class CallStatus: 
    INI = 'INI' #initiated
    RUN = 'RUN' #running
    WAI = 'WAI' #waiting (e.g. for user input)
    ABO = 'ABO' #aborted
    ERR = 'ERR' #error
    FIN = 'FIN' #finished (sucesfully)
 
'''
 CALL 
''' 
class Call: 
    def __init__(self,callId,name,handler,ctype,status=CallStatus.INI):
        self.callId = callId
        self.name = name
        self.handler = handler
        self.ctype = ctype
        self.status = status
        self.outputs= {}
        self.value = None
        
        