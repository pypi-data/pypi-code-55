#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class License:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection

    def describe(self, entitlement=None):
        if entitlement:
            params = {'entitlement': entitlement}
        else:
            params = None
        return self._connection.get(url='/license', params=params)