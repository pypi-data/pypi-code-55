#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class WebHook:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##Sessions
    def list(self, limit=25, expand="all"):
        url = '/webhooks'
        params={'limit': limit, 'expand':expand}

        rtv = self._connection.get(url=url, params=params)
        items = rtv['webhooks']
        while "next" in rtv:
            params['cursor']= rtv['next']
            rtv = self._connection.get(url=url, params=params)
            items.extend(rtv['webhooks'])
        return items
    def create(self, payload):
        return self._connection.post(url='/webhooks', data=payload)
    def describe(self, id):
        return self._connection.get(url='/webhooks/' + str(id))
    def modify(self, id, payload):
        return self._connection.post(url='/webhooks' + str(id), data=payload)
    def delete(self, id):
        return self._connection.delete(url='/webhooks/' + str(id))
    def modify(self, id):
        return self._connection.post(url='/webhooks' + str(id) +"/ping", data=None)

