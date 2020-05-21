#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class Users:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##Users
    def list(self, limit=25, expand="all", query=""):
        params={'limit': limit, 'expand':expand,'query':query}
        rtv = self._connection.get(url='/users', params=params)
        items = rtv['users']
        while "next" in rtv:
            params={'limit': limit, 'expand':expand,'query':query, 'cursor': rtv['next']}
            rtv = self._connection.get(url='/users', params=params)
            items.extend(rtv['users'])
        return items
    def create(self, payload):
        return self._connection.post(url='/users', data=payload)
    def describe(self, id, expand="all"):
        params = {'expand': expand}
        return self._connection.get(url='/users/' + str(id), params=params )
    def modify(self,id, payload):
        return self._connection.post(url='/users/' + str(id), data=payload)
    def delete(self, id):
        return self._connection.delete(url='/users/' + str(id))
    def changePassword(self,id, payload):
        return self._connection.post(url='/users/' + str(id)+"/password", data=payload)
