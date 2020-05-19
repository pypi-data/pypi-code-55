#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

#import connect
#import config

class ScheduledTasks:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##ScheduledTasks
    def list(self):
        return self._connection.get(url='/scheduledtasks')
    def create(self, payload):
        return self._connection.post(url='/scheduledtasks', data=payload)
    def search(self, payload):
        return self._connection.post(url='/scheduledtasks/search', data=payload)
    def describe(self, scheduledtaskID):
        return self._connection.get(url='/scheduledtasks/' + str(scheduledtaskID))
    def modify(self, scheduledtaskID, payload):
        return self._connection.post(url='/scheduledtasks/' + str(scheduledtaskID), data=payload)
    def delete(self, scheduledtaskID):
        return self._connection.delete(url='/scheduledtasks/' + str(scheduledtaskID))
