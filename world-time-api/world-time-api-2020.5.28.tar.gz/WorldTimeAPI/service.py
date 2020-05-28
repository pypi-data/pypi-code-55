import requests as req
import json
from WorldTimeAPI.schemas import *

class Client:
    """
    Create a WorldtimeAPI client for a specified endpoint
    
    Supported endpoints are 'timezone' and 'ip'
    """
    def __init__(self,endpoint):
        if not isinstance(endpoint,str):
            raise TypeError("Endpoint must be a string.")
        if not (endpoint in ('timezone','ip')):
            raise ValueError(f"{endpoint} not in available endpoint list ('timezone','ip').")
        
        # for the timezone endpoint, define a regions list property
        if endpoint == 'timezone':
            self.regions = lambda: self.get(**{})
        
        self._url = "http://worldtimeapi.org/api/" + endpoint
    
    def get(self,**payload):
        checkPayload(payload)    
        params = ('area','location','region')
        keys = payload.keys()
        args = ''
        
        for item in keys:
            if not (item in params):
                raise KeyError(f"{item} not a valid payload parameter.")
        
        if ('area' in keys):
            args += '/' + payload['area']
        if ('location' in keys):
            args += '/' + payload['location']
        if ('region' in keys):
            args += '/' + payload['region']

        response = req.get(self._url + args).json()
        
        if isinstance(response,dict):
            try:
                return ErrorJson(**response)
            except:
                return DateTimeJson(**response)
        return ListJson(*response) 
            
    @property
    def url(self):
        return self._url

def checkPayload(payload):
        if not isinstance(payload,dict):
            raise TypeError(f"payload type {type(payload)} not of type {type(dict)}")
        if len(payload) > 3:
            raise ValueError(f"Recieved {len(payload)} payload arguments. Expected 3 or fewer.")
        for key,item in payload.items():
            if not (isinstance(key,str) or isinstance(item,str)):
                raise TypeError("Expected payload key and item types str")
