#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class firewall:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##Firewall rules
    def list(self):
        return self._connection.get(url='/firewallrules')
    def create(self, payload):
        return self._connection.post(url='/firewallrules', data=payload)
    def describe(self, firewallRuleID):
        return self._connection.get(url='/firewallrules/' + str(firewallRuleID))
    def modify(self, firewallRuleID, payload):
        return self._connection.post(url='/firewallrules/' + str(firewallRuleID), data=payload)
    def delete(self, firewallRuleID):
        return self._connection.delete(url='/firewallrules/' + str(firewallRuleID))
    def search(self, payload):
        return self._connection.post(url='/firewallrules/search', data=payload)
    ##Interface Type
    def listInterfaceTypes(self, policyID):
        return self._connection.get(url='/policies/'+str(policyID)+'/interfacetypes')
    def createInterfaceType(self,policyID, payload):
        return self._connection.post(url='/policies/'+str(policyID)+"/interfacetypes", data=payload)
    def describeInterfaceType(self, policyID, interfaceTypeID):
        return self._connection.get(url='/policies/' + str(policyID) + '/interfacetypes/'+ str(interfaceTypeID))
    def modifyInterfaceType(self, policyID, interfaceTypeID, payload):
        return self._connection.post(url='/policies/' + str(policyID) + '/interfacetypes/'+ str(interfaceTypeID), data=payload)
    def deleteInterfaceType(self,  policyID, interfaceTypeID,):
        return self._connection.delete(url='/policies/' + str(policyID) + '/interfacetypes/'+ str(interfaceTypeID))
    def searchInterfaceTypes(self, policyID, payload):
        return self._connection.post(url='/policies/'+str(policyID)+'/interfacetypes/search', data=payload)
    ##Firewall IP list
    def listIPLists(self):
        return self._connection.get(url='/iplists')
    def createiplists(self, payload):
        return self._connection.post(url='/iplists', data=payload)
    def describeIPList(self, ipListID):
        return self._connection.get(url='/iplists/' + str(ipListID))
    def modifyIPList(self, ipListID, payload):
        return self._connection.post(url='/iplists/' + str(ipListID), data=payload)
    def deleteIPList(self, ipListID):
        return self._connection.delete(url='/iplists/' + str(ipListID))
    def searchIPLists(self, payload):
        return self._connection.post(url='/iplists/search', data=payload)
    ##Firewall MAC list
    def listMacLists(self):
        return self._connection.get(url='/maclists')
    def createmaclists(self, payload):
        return self._connection.post(url='/maclists', data=payload)
    def describemacList(self, macListID):
        return self._connection.get(url='/maclists/' + str(macListID))
    def modifymacList(self, macListID, payload):
        return self._connection.post(url='/maclists/' + str(macListID), data=payload)
    def deletemacList(self, macListID):
        return self._connection.delete(url='/maclists/' + str(macListID))
    def searchmacLists(self, payload):
        return self._connection.post(url='/maclists/search', data=payload)
    ##Firewall Port list
    def listPortLists(self):
        return self._connection.get(url='/portlists')
    def createportlists(self, payload):
        return self._connection.post(url='/portlists', data=payload)
    def describeportList(self, portListID):
        return self._connection.get(url='/portlists/' + str(portListID))
    def modifyportList(self, portListID, payload):
        return self._connection.post(url='/portlists/' + str(portListID), data=payload)
    def deleteportList(self, portListID):
        return self._connection.delete(url='/portlists/' + str(portListID))
    def searchportLists(self, payload):
        return self._connection.post(url='/portlists/search', data=payload)
    ##Firewall Contexts
    def listContexts(self):
        return self._connection.get(url='/contexts')
    def createContext(self, payload):
        return self._connection.post(url='/contexts', data=payload)
    def describeContext(self, contextID):
        return self._connection.get(url='/contexts/' + str(contextID))
    def modifyContext(self, contextID, payload):
        return self._connection.post(url='/contexts/' + str(contextID), data=payload)
    def deleteContext(self, contextID):
        return self._connection.delete(url='/contexts/' + str(contextID))
    def searchContexts(self, payload):
        return self._connection.post(url='/contexts/search', data=payload)
    ##Firewall Stateful Configurations
    def listStatefulConfigurations(self):
        return self._connection.get(url='/statefulconfigurations')
    def createStatefulConfiguration(self, payload):
        return self._connection.post(url='/statefulconfigurations', data=payload)
    def describeStatefulConfiguration(self, statefulConfigurationID):
        return self._connection.get(url='/statefulconfigurations/' + str(statefulConfigurationID))
    def modifyStatefulConfiguration(self, statefulConfigurationID, payload):
        return self._connection.post(url='/statefulconfigurations/' + str(statefulConfigurationID), data=payload)
    def deleteStatefulConfiguration(self, statefulConfigurationID):
        return self._connection.delete(url='/statefulconfigurations/' + str(statefulConfigurationID))
    def searchStatefulConfigurations(self, payload):
        return self._connection.post(url='/statefulconfigurations/search', data=payload)



