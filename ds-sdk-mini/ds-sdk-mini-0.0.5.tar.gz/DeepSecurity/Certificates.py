#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

#import connect
#import config

class Certificates:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##Certificates
    def describe(self, certID):
        return self._connection.get(url='/certificates/' + str(certID))
    def delete(self, certID):
        return self._connection.delete(url='/certificates/' + str(certID))
    def getByURL(self, url):
        params = {'URL' : str(url)}
        return self._connection.get(url='/certificates/target', params=params )
    def list(self):
        return self._connection.get(url='/certificates')
    def add(self, payload):
        return self._connection.post(url='/certificates', data=payload)

