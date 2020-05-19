#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

#import connect
#import config

class ReportTemplates:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##EventBasedTasks
    def list(self):
        return self._connection.get(url='/reporttemplates')
    def search(self, payload):
        return self._connection.post(url='/reporttemplates/search', data=payload)
    def describe(self, reportID):
        return self._connection.get(url='/reporttemplates/' + str(reportID))

