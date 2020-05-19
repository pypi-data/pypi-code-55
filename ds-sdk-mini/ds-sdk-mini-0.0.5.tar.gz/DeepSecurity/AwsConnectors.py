#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class AwsConnectors:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##connectors
    def list(self):
        return self._connection.get(url='/awsconnectors')
    def create(self, payload):
        return self._connection.post(url='/awsconnectors', data=payload)
    def describe(self, connectorID):
        return self._connection.get(url='/awsconnectors/' + str(connectorID))
    def modify(self, connectorID, payload):
        return self._connection.post(url='/awsconnectors/' + str(connectorID), data=payload)
    def delete(self, connectorID):
        return self._connection.delete(url='/awsconnectors/' + str(connectorID))
    def search(self, payload):
        return self._connection.send(url='/awsconnectors/search', data=payload)
    def Settings(self):
        return self._connection.get(url='/awsconnectorsettings')