#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class Sessions:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##Sessions
    def list(self, limit=25, expand="all", query=""):
        params={'limit': limit, 'expand':expand,'query':query}
        rtv = self._connection.get(url='/sessions', params=params)
        items = rtv['sessions']
        while "next" in rtv:
            params={'limit': limit, 'expand':expand,'query':query, 'cursor': rtv['next']}
            rtv = self._connection.get(url='/sessions', params=params)
            items.extend(rtv['sessions'])
        return items
    def create(self, payload):
        return self._connection.post(url='/sessions', data=payload)
    def describe(self, id, expand="all"):
        params = {'expand': expand}
        return self._connection.get(url='/sessions/' + str(id), params=params )
    def refresh(self, id):
        return self._connection.post(url='/sessions/' + str(id), data="")
    def delete(self, id):
        return self._connection.delete(url='/sessions/' + str(id))
