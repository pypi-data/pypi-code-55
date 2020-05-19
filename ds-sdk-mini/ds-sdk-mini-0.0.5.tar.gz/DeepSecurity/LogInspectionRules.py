#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class LogInspectionRules:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##LogInspection rules
    def list(self):
        return self._connection.get(url='/loginspectionrules')
    def create(self, payload):
        return self._connection.post(url='/loginspectionrules', data=payload)
    def describe(self, logInspectionRuleID):
        return self._connection.get(url='/loginspectionrules/' + str(logInspectionRuleID))
    def modify(self, logInspectionRuleID, payload):
        return self._connection.post(url='/loginspectionrules/' + str(logInspectionRuleID), data=payload)
    def delete(self, logInspectionRuleID):
        return self._connection.delete(url='/loginspectionrules/' + str(logInspectionRuleID))
    def search(self, payload):
        return self._connection.post(url='/loginspectionrules/search', data=payload)