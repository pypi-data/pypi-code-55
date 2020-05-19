#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

#import connect
#import config

class Tenants:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##SystemSettings
    def list(self):
        return self._connection.get(url='/tenants')
    def modify(self, tenantID, payload):
        return self._connection.post(url='/tenants/' + str(tenantID), data=payload)
    def describe(self, tenantID):
        return self._connection.get(url='/tenants/' + str(tenantID))
    def delete(self, tenantID):
        return self._connection.delete(url='/tenants/' + str(tenantID))
    def create(self, payload):
        return self._connection.post(url='/tenants', data=payload)
    def search(self, payload):
        return self._connection.post(url='/tenants/search', data=payload)
    def createAPIKey(self, tenantID, payload):
        return self._connection.post(url='/tenants/' + str(tenantID), data=payload)


