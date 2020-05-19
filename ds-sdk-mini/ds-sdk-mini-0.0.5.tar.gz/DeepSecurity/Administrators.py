#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class Administrators:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##Administrators
    def list(self):
        return self._connection.get(url='/administrators')
    def create(self, payload):
        return self._connection.post(url='/administrators', data=payload)
    def describe(self, adminID):
        return self._connection.get(url='/administrators/' + str(adminID))
    def modify(self, adminID, payload):
        return self._connection.post(url='/administrators/' + str(adminID), data=payload)
    def delete(self, adminID):
        return self._connection.delete(url='/administrators/' + str(adminID))
    def search(self, payload):
        return self._connection.post(url='/administrators/search', data=payload)
    #Roles
    def listRoles(self):
        return self._connection.get(url='/roles')
    def createRole(self, payload):
        return self._connection.post(url='/roles', data=payload)
    def searchRole(self, payload):
        return self._connection.post(url='/roles/search', data=payload)
    def describeRole(self, roleID):
        return self._connection.get(url='/roles/' + str(roleID))
    def modifyRole(self, roleID, payload):
        return self._connection.post(url='/roles/' + str(roleID), data=payload)
    def deleteRole(self, roleID):
        return self._connection.delete(url='/roles/' + str(roleID))

