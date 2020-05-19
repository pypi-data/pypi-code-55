#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

#import connect
#import config

class Computers:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##Computers
    def list(self, expand=None, overrides=None):
        params = {}
        if expand:
            params['expand'] = expand
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers', params=params)
    def describe(self, id, expand=None, overrides=None):
        params = {}
        if expand:
            params['expand'] = expand
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/' + str(id), params=params)
    def modify(self, id, expand=None, overrides=None, payload=None):
        params = {}
        if expand:
            params['expand'] = expand
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/' + str(id), data=payload, params=params)
    def delete(self, id):
        return self._connection.delete(url='/computers/' + str(id))
    def describeSetting(self, id, setting, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/' + str(id) + '/settings/' + str(setting), params=params)
    def modifySetting(self, id, setting, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/' + str(id) + '/settings/' + setting, data=payload, params=params)
    def resetSetting(self, id, setting, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/' + str(id) + '/settings/' + setting, params=params)
    def create(self, expand=None, overrides=None, payload=None):
        params = {}
        if expand:
            params['expand'] = expand
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers' , data=payload, params=params)
    def search(self, expand=None, overrides=None, payload=None):
        url = '/computers/search'
        computers = None
        params = {}
        if expand:
            params['expand'] = expand
        if overrides:
            params['overrides'] = overrides
        rtv = self._connection.post(url=url, data=payload, params=params)
        if 'computers' not in rtv:
            return rtv
        computers = rtv['computers']
        while len(rtv['computers']) > 0:
            if 'idTest' in payload['searchCriteria']:
                if payload['searchCriteria']['idTest'] == 'equal'  or payload['searchCriteria']['idTest'] == 'not-equal':
                    return computers
                if payload['searchCriteria']['idTest'] == 'greater-than-or-equal':
                    payload['searchCriteria']['idValue'] = int(computers[len(computers) - 1]['ID'])+1
                if payload['searchCriteria']['idTest'] == 'less-than-or-equal':
                    payload['searchCriteria']['idValue'] = int(computers[len(computers)-1]['ID'])-1
                if payload['searchCriteria']['idTest'] == 'less-than' or payload['searchCriteria']['idTest'] == 'greater-than':
                    payload['searchCriteria']['idValue'] = int(computers[len(computers) - 1]['ID'])
            rtv = self._connection.post(url=url, data=payload, params=params)
            computers.extend(rtv['computers'])
        return computers


    ##Computers Firewall Rule Assignments
    def listFirewallAssignment(self, id, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/' + str(id) + '/firewall/assignments', params=params)
    def addFirewallAssignment(self, id, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/' + str(id) + '/firewall/assignments', data=payload, params=params)
    def setFirewallAssignment(self, id, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.put(url='/computers/' + str(id) + '/firewall/assignments', data=payload, params=params)
    def deleteFirewallAssignment(self, id, ruleID, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/' + str(id) + '/firewall/assignments/'+ruleID, params=params)
    ##Computers Firewall Rule
    def listFirewallRules(self, id, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/' + str(id) + '/firewall/rules', params=params)
    def describeFirewallRules(self, id, firewallRuleId, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/' + str(id) + '/firewall/rules/'+firewallRuleId, params=params)
    def modifyFirewallRules(self, id, firewallRuleId, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/' + str(id) + '/firewall/rules/'+firewallRuleId, data=payload, params=params)
    def resetFirewallRules(self, id, firewallRuleId, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/' + str(id) + '/firewall/rules/'+firewallRuleId, params=params)
    #IntegrityMonitoring
    def listIntegrityMonitoringRules(self, id, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/' + str(id) + '/integritymonitoring/rules', params=params)
    def describeIntegrityMonitoringRules(self, id, fintegritymonitoringlRuleId, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/' + str(id) + '/integritymonitoring/rules/' + str(fintegritymonitoringlRuleId), params=params)
    def modifyIntegrityMonitoringRules(self, id, fintegritymonitoringlRuleId, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/' + str(id) + '/integritymonitoring/rules/' + str(fintegritymonitoringlRuleId), data=payload, params=params)
    def deleteIntegrityMonitoringRules(self, id, fintegritymonitoringlRuleId, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/' + str(id) + '/integritymonitoring/rules/' + str(fintegritymonitoringlRuleId), params=params)
    #Intrusion Prevention - assignments
    def listIntrusionPreventionAssignment(self, id, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/' + str(id) + '/intrusionprevention/assignments', params=params)
    def assignIntrusionPreventionAssignment(self, id, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/' + str(id) + '/intrusionprevention/assignments', data=payload, params=params)
    def createIntrusionPreventionAssignment(self, id, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.put(url='/computers/' + str(id) + '/intrusionprevention/assignments', data=payload, params=params)
    def deleteComputerIntrusionPreventionAssignment(self, id, ruleID, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/' + str(id) + '/intrusionprevention/assignments/'+str(ruleID), params=params)
    #Intrusion Prevention - application type
    def listIntrusionPreventionApplicationTypes(self, id, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/' + str(id) + '/intrusionprevention/applicationtypes', params=params)
    def describeIntrusionPreventionApplicationTypes(self, id, intrusionPreventionApplicationTypesId, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/' + str(id) + '/intrusionprevention/applicationtypes/'+ str(intrusionPreventionApplicationTypesId), params=params)
    def modifyIntrusionPreventionApplicationTypes(self, id, intrusionPreventionApplicationTypesId, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/' + str(id) + '/intrusionprevention/applicationtypes/' + str(intrusionPreventionApplicationTypesId), data=payload, params=params)
    def deleteIntrusionPreventionApplicationTypes(self, id, intrusionPreventionApplicationTypesId, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/' + str(id) + '/intrusionprevention/applicationtypes/' + str(intrusionPreventionApplicationTypesId), params=params)
    #Intrusion Prevention - Rule
    def listIntrusionPreventionRules(self, id, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/' + str(id) + '/intrusionprevention/rules', params=params)
    def describeIntrusionPreventionRule(self, id, ruleID, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/' + str(id) + '/intrusionprevention/rules/'+ str(ruleID), params=params)
    def modifyIntrusionPreventionRule(self, id, ruleID, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/' + str(id) + '/intrusionprevention/rules/' + str(ruleID), data=payload, params=params)
    def deleteIntrusionPreventionRules(self, id, ruleID, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/' + str(id) + '/intrusionprevention/rules/' + str(ruleID), params=params)
    #Log Inspection assignment
    def listLogInspectionAssignment(self, id, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/' + str(id) + '/loginspection/assignments', params=params)
    def assignLogInspectionAssignment(self, id, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/' + str(id) + '/loginspection/assignments', params=params, data=payload)
    def setLogInspectionAssignment(self, id, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.put(url='/computers/' + str(id) + '/loginspection/assignments', params=params, data=payload)
    def deleteLogInspectionAssignment(self, id, ruleID, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/' + str(id) + '/loginspection/assignments/'+str(ruleID), params=params)
    #ILog Inspection  - rules
    def listLogInspectionRules(self, id, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/' + str(id) + '/loginspection/rules', params=params)
    def describeLogInspectionRule(self, id, ruleID, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/' + str(id) + '/loginspection/rules/' + str(ruleID), params=params)
    def modifyLogInspectionRule(self, id, ruleID, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/' + str(id) + '/loginspection/rules/' + str(ruleID), data=payload, params=params)
    def deleteLogInspectionRule(self, id, ruleID, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/' + str(id) + '/loginspection/rules/' + str(ruleID), params=params)



