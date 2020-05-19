#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class IntegrityMonitoring:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##IntegrityMonitoring config
    def list(self):
        return self._connection.get(url='/integritymonitoringrules')
    def create(self, payload):
        return self._connection.post(url='/integritymonitoringrules', data=payload)
    def describe(self, integrityMonitoringRuleID):
        return self._connection.get(url='/integritymonitoringrules/' + str(integrityMonitoringRuleID))
    def modify(self, integrityMonitoringRuleID, payload):
        return self._connection.post(url='/integritymonitoringrules/' + str(integrityMonitoringRuleID), data=payload)
    def delete(self, integrityMonitoringRuleID):
        return self._connection.delete(url='/integritymonitoringrules/' + str(integrityMonitoringRuleID))
    def search(self, payload):
        return self._connection.post(url='/integritymonitoringrules/search', data=payload)