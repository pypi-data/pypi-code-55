#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class Roles:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##Sessions
    def list(self, limit=25, expand="all", query=""):
        params={'limit': limit, 'expand':expand,'query':query}
        rtv = self._connection.get(url='/roles', params=params)
        items = rtv['roles']
        while "next" in rtv:
            params={'limit': limit, 'expand':expand,'query':query, 'cursor': rtv['next']}
            rtv = self._connection.get(url='/roles', params=params)
            items.extend(rtv['roles'])
        return items
    def create(self, payload):
        return self._connection.post(url='/roles', data=payload)
    def describe(self, id, expand="all"):
        params = {'expand': expand}
        return self._connection.get(url='/roles/' + str(id), params=params )
    def modify(self,id, payload):
        return self._connection.post(url='/roles/' + str(id), data=payload)
    def deleteSession(self, id):
        return self._connection.delete(url='/roles/' + str(id))
