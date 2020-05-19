#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

#import connect
#import config

class ComputerGroups:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##ComputerGroups
    def list(self):
        return self._connection.get(url='/computergroups')
    def create(self, payload):
        return self._connection.post(url='/computergroups', data=payload)
    def search(self, payload):
        return self._connection.post(url='/computergroups/search', data=payload)
    def describe(self, groupID):
        return self._connection.get(url='/computergroups/' + str(groupID))
    def modify(self, id, payload):
        return self._connection.post(url='/computergroups/' + str(id), data=payload)
    def delete(self, id):
        return self._connection.delete(url='/computergroups/' + str(id))



