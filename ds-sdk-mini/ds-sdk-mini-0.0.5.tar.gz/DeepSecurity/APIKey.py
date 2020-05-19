#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

#import connect
#import config

class APIKeys:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##APIKeys
    def Current(self):
        return self._connection.get(url='/apikeys/current')
    def modifyCurrent(self, payload):
        return self._connection.post(url='/apikeys/current', data=payload)
    def currentSecretKey(self, payload):
        return self._connection.post(url='/apikeys/current/secretkey', data=payload)
    def describe(self, apikeyID):
        return self._connection.get(url='/apikeys/' + str(apikeyID))
    def modify(self, apikeyID, payload):
        return self._connection.post(url='/apikeys/' + str(apikeyID), data=payload)
    def delete(self, apikeyID):
        return self._connection.delete(url='/apikeys/' + str(apikeyID))
    def generateSecret(self, apikeyID, payload):
        return self._connection.post(url='/apikeys/' + str(apikeyID) +'/secretkey', data=payload)
    def list(self):
        return self._connection.get(url='/apikeys')
    def create(self, payload):
        return self._connection.post(url='/apikeys', data=payload)
    def search(self, payload):
        return self._connection.post(url='/apikeys/search', data=payload)


