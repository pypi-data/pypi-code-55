#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class ApplicationControl:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##ApplicationControl global rules
    def listGlobalRules(self):
        return self._connection.get(url='/applicationcontrolglobalrules')
    def createGlobalRule(self, payload):
        return self._connection.post(url='/applicationcontrolglobalrules', data=payload)
    def describeGlobalRule(self, ruleID):
        return self._connection.get(url='/applicationcontrolglobalrules/' + str(ruleID))
    def modifyGlobalRule(self, ruleID, payload):
        return self._connection.post(url='/applicationcontrolglobalrules/' + str(ruleID), data=payload)
    def deleteGlobalRule(self, ruleID):
        return self._connection.delete(url='/applicationcontrolglobalrules/' + str(ruleID))
    def searchGlobalRules(self, payload):
        return self._connection.post(url='/applicationcontrolglobalrules/search', data=payload)
    ## ApplicationControl
    def listrulesets(self):
        return self._connection.get(url='/rulesets')
    def createruleset(self, payload):
        return self._connection.post(url='/rulesets', data=payload)
    def describeGlobalRule(self, rulesetID):
        return self._connection.get(url='/rulesets/' + str(rulesetID))
    def modifyruleset(self, rulesetID, payload):
        return self._connection.post(url='/rulesets/' + str(rulesetID), data=payload)
    def deleteruleset(self, rulesetID):
        return self._connection.delete(url='/rulesets/' + str(rulesetID))
    def searchrulesets(self, payload):
        return self._connection.post(url='/rulesets/search', data=payload)
    def listrulesetRules(self, rulesetID):
        return self._connection.get(url='/rulesets/'+str(rulesetID)+'/rules')
    def describeRulesetRule(self, rulesetID, ruleID):
        return self._connection.get(url='/rulesets/' + str(rulesetID)+'/rules/'+str(ruleID))
    def modifyrulesetRule(self, rulesetID, ruleID, payload):
        return self._connection.post(url='/rulesets/' + str(rulesetID)+'/rules/'+str(ruleID), data=payload)
    def deleterulesetRule(self, rulesetID, ruleID):
        return self._connection.delete(url='/rulesets/' + str(rulesetID)+'/rules/'+str(ruleID))
    def searchrulesetRules(self, rulesetID, payload):
        return self._connection.post(url='/rulesets/' + str(rulesetID) + '/search', data=payload)
    ## Software Changes
    def listsoftwareChanges(self):
        return self._connection.get(url='/softwarechanges')
    def describesoftwareChange(self, softwareChangeID):
        return self._connection.get(url='/softwarechanges/' + str(softwareChangeID))
    def searchsoftwareChanges(self, payload):
        return self._connection.post(url='/softwarechanges/search', data=payload)
    def reviewSoftwareChange(self, payload):
        return self._connection.post(url='/softwarechanges/review', data=payload)
    ## Software Inventories
    def listSoftwareInventories(self):
        return self._connection.get(url='/softwareinventories')
    def createSoftwareInventory(self, payload):
        return self._connection.post(url='/softwareinventories', data=payload)
    def describeSoftwareInventory(self, softwareInventoryID):
        return self._connection.get(url='/softwareinventories/' + str(softwareInventoryID))
    def deleteSoftwareInventory(self, softwareInventoryID):
        return self._connection.delete(url='/softwareinventories/' + str(softwareInventoryID))
    def searchSoftwareInventory(self, payload):
        return self._connection.post(url='/softwareinventories/search', data=payload)
    def listSoftwareInventoryItems(self,softwareInventoryID):
        return self._connection.get(url='/softwareinventories/'+str(softwareInventoryID)+'/items')
    def searchSoftwareInventoryItems(self, softwareInventoryID, payload):
        return self._connection.post(url='/softwareinventories/'+str(softwareInventoryID)+'/items/search', data=payload)
    def describeSoftwareInventoryItem(self,softwareInventoryID, inventoryItemID):
        return self._connection.get(url='/softwareinventories/'+str(softwareInventoryID)+'/items/' + str(inventoryItemID))

