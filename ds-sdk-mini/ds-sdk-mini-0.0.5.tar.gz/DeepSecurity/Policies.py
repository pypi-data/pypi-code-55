#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

#import connect
#import config

class Policies:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##Policies
    def list(self):
        return self._connection.get(url='/policies')
    def create(self, payload):
        return self._connection.post(url='/policies', data=payload)
    def describe(self, id):
        return self._connection.get(url='/policies/' + str(id))
    def modify(self, id, payload):
        return self._connection.post(url='/policies/' + str(id), data=payload)
    def delete(self, id):
        return self._connection.delete(url='/policies/' + str(id))
    def search(self, overrides=False, payload=""):
        url = '/policies/search'
        if overrides:
            url = url + "?overrides=True"
        return self._connection.post(url=url, data=payload)
    # Default Policy Setting
    def describeDefaultSetting(self, name):
        return self._connection.get(url='/policies/default/settings/' + str(name))
    def modifyDefaultSetting(self, name, payload):
        return self._connection.post(url='/policies/default/settings/' + str(name), data=payload)
    def deleteDefaultSetting(self, name):
        return self._connection.delete(url='/policies/default/settings/' + str(name))
    #Default Policy
    def listPolicyDefault(self):
        return self._connection.get(url='/policies/default')
    def modifyPolicyDefault(self, payload):
        return self._connection.post(url='/policies/default', data=payload)
    def describePolicyDefault(self, policyID, name):
        return self._connection.get(url='/policies/' + policyID + '/settings/' + str(name))
    def modifyPolicySetting(self, policyID, name, payload):
        return self._connection.post(url='/policies/' + policyID + '/settings/' + str(name), data=payload)
    def resetPolicySetting(self, policyID, name):
        return self._connection.delete(url='/policies/' + policyID + '/settings/' + str(name))
    #Policy Firewall assignments
    def listFirewallRulesAssignments(self, policyID):
        return self._connection.get(url='/policies/' + policyID + '/firewall/assignments')
    def AddFirewallRuleAssignments(self, policyID, payload):
        return self._connection.post(url='/policies/' + policyID + '/firewall/assignments', data=payload)
    def SetFirewallRulesAssignments(self, policyID, payload):
        return self._connection.put(url='/policies/' + policyID + '/firewall/assignments', data=payload)
    def deleteFirewallRuleAssignments(self, policyID, firewallID):
        return self._connection.delete(url='/policies/' + policyID + '/firewall/assignments/' + str(firewallID))
    # Policy Firewall
    def listFirewallRules(self, policyID):
        return self._connection.get(url='/policies/' + policyID + '/firewall/rules')
    def describeFirewallRules(self, policyID, firewallID):
        return self._connection.get(url='/policies/' + policyID + '/firewall/rules/' + str(firewallID))
    def modifyFirewallRules(self, policyID, firewallID, payload):
        return self._connection.post(url='/policies/' + policyID + '/firewall/rules/' + str(firewallID), data=payload)
    def resetFirewallRules(self, policyID, firewallID):
        return self._connection.delete(url='/policies/' + policyID + '/firewall/rules/' + str(firewallID))
    # Integrity monitoring assignments
    def listIntegrityMonitoringRulesAssignments(self, policyID):
        return self._connection.get(url='/policies/' + policyID + '/integritymonitoring/assignments')
    def addIntegrityMonitoringRuleAssignments(self, policyID, payload):
        return self._connection.post(url='/policies/' + policyID + '/integritymonitoring/assignments', data=payload)
    def setIntegrityMonitoringRuleAssignments(self, policyID, payload):
        return self._connection.put(url='/policies/' + policyID + '/integritymonitoring/assignments', data=payload)
    def removeIntegrityMonitoringRuleAssignments(self, policyID, integritymonitoringID):
        return self._connection.delete(url='/policies/' + policyID + '/integritymonitoring/assignments/' + str(integritymonitoringID))
    # Integrity monitoring
    def listIntegrityMonitoringRules(self, policyID):
        return self._connection.get(url='/policies/' + policyID + '/integritymonitoring/rules')
    def describeIntegrityMonitoringRules(self, policyID, integritymonitoringID):
        return self._connection.get(url='/policies/' + policyID + '/integritymonitoring/rules/' + str(integritymonitoringID))
    def modifyIntegrityMonitoringRules(self, policyID, integritymonitoringID, payload):
        return self._connection.post(url='/policies/' + policyID + '/integritymonitoring/rules/' + str(integritymonitoringID), data=payload)
    def deleteIntegrityMonitoringRules(self, policyID, integritymonitoringID):
        return self._connection.delete(url='/policies/' + policyID + '/integritymonitoring/rules/' + str(integritymonitoringID))
    # Intrusion Prevention assignments
    def listIntrusionPreventionRulesAssignments(self, policyID):
        return self._connection.get(url='/policies/' + policyID + '/intrusionprevention/assignments')
    def AddIntrusionPreventionRuleAssignments(self, policyID, payload):
        return self._connection.post(url='/policies/' + policyID + '/intrusionprevention/assignments', data=payload)
    def SetIntrusionPreventionRulesAssignments(self, policyID, payload):
        return self._connection.put(url='/policies/' + policyID + '/intrusionprevention/assignments', data=payload)
    def deleteIntrusionPreventionRuleAssignments(self, policyID, intrusionpreventionID):
        return self._connection.delete(url='/policies/' + policyID + '/intrusionprevention/assignments/' + str(intrusionpreventionID))
    # Intrusion Prevention
    def listIntrusionPreventionRules(self, policyID):
        return self._connection.get(url='/policies/' + policyID + '/intrusionprevention/rules')
    def describeIntrusionPreventionRules(self, policyID, intrusionpreventionID):
        return self._connection.get(url='/policies/' + policyID + '/intrusionprevention/rules/' + str(intrusionpreventionID))
    def modifyIntrusionPreventionRules(self, policyID, intrusionpreventionID, payload):
        return self._connection.post(url='/policies/' + policyID + '/intrusionprevention/rules/' + str(intrusionpreventionID), data=payload)
    def resetIntrusionPreventionRules(self, policyID, intrusionpreventionID):
        return self._connection.delete(url='/policies/' + policyID + '/intrusionprevention/rules/' + str(intrusionpreventionID))
    # Intrusion Prevention application
    def listIntrusionPreventionApplication(self, policyID):
        return self._connection.get(url='/policies/' + policyID + '/intrusionprevention/applicationtypes')
    def describeIntrusionPreventionApplication(self, policyID, applicationID):
        return self._connection.get(url='/policies/' + policyID + '/intrusionprevention/applicationtypes/' + str(applicationID))
    def modifyIntrusionPreventionApplication(self, policyID, applicationID, payload):
        return self._connection.post(url='/policies/' + policyID + '/intrusionprevention/applicationtypes/' + str(applicationID), data=payload)
    def resetIntrusionPreventionApplication(self, policyID, applicationID):
        return self._connection.delete(url='/policies/' + policyID + '/intrusionprevention/applicationtypes/' + str(applicationID))
    #Log inspection assignments
    def listLogInspectionRulesAssignments(self, policyID):
        return self._connection.get(url='/policies/' + policyID + '/loginspection/assignments')
    def AddLogInspectionRuleAssignments(self, policyID, payload):
        return self._connection.post(url='/policies/' + policyID + '/loginspection/assignments', data=payload)
    def SetLogInspectionRulesAssignments(self, policyID, payload):
        return self._connection.put(url='/policies/' + policyID + '/loginspection/assignments', data=payload)
    def deleteLogInspectionRuleAssignments(self, policyID, loginspectionID):
        return self._connection.delete(url='/policies/' + policyID + '/loginspection/assignments/' + str(loginspectionID))
    #Log Inspection
    def listLogInspection(self, policyID):
        return self._connection.get(url='/policies/' + policyID + '/loginspection/rules')
    def describeLogInspection(self, policyID, applicationD):
        return self._connection.get(url='/policies/' + policyID + '/loginspection/rules/' + str(applicationD))
    def modifyLogInspection(self, policyID, applicationD, payload):
        return self._connection.post(url='/policies/' + policyID + '/loginspection/rules/' + str(applicationD), data=payload)
    def resetLogInspection(self, policyID, loginspectionID):
        return self._connection.delete(url='/policies/' + policyID + '/loginspection/rules/' + str(loginspectionID))


