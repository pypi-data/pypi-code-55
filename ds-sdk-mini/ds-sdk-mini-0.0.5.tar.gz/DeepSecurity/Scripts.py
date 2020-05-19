#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

#import connect
#import config

class Scripts:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##ScheduledTasks
    def list(self):
        return self._connection.get(url='/scripts')
