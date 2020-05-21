#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class ContentRules:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    def listContentRulesetCollections(self, limit=25, expand="all", query=None):
        url = "/collections"
        params={'limit': limit, 'expand':expand}
        if query:
            params['query'] = query
        rtv = self._connection.get(url=url, params=params)
        items = rtv['collections']
        while "next" in rtv:
            params['cursor'] = rtv['next']
            rtv = self._connection.get(url=url, params=params)
            items.extend(rtv['collections'])
        return items
    def createContentRulesetCollection(self, payload):
        return self._connection.post(url='/collections', data=payload)
    def describeContentRulesetCollection(self, id):
        return self._connection.get(url='/collections/' + str(id))
    def modifyContentRulesetCollection(self, id, data):
        return self._connection.post(url='/collections/' + str(id), payload=data)
    def deleteContentRulesetCollection(self, id):
        return self._connection.delete(url='/collections/' + str(id))
    def listContentRuleset(self, id, limit=25,  query=None):
        url = "/collections/"+str(id)+'/rulesets'
        params={'limit': limit}
        if query:
            params['query'] = query
        rtv = self._connection.get(url=url, params=params)
        items = rtv['rulesets']
        while "next" in rtv:
            params['cursor']= rtv['next']
            rtv = self._connection.get(url=url, params=params)
            items.extend(rtv['rulesets'])
        return items
    def createContentRuleset(self, id, payload):
        return self._connection.post(url='/collections/'+str(id)+'/rulesets', data=payload)
    def describeContentRuleset(self, id,rulesetID):
        return self._connection.get(url='/collections/' + str(id)+'/rulesets/'+str(rulesetID))
    def modifyContentRuleset(self, id, rulesetID, data):
        return self._connection.post(url='/collections/' + str(id)+'/rulesets/'+str(rulesetID), payload=data)
    def deleteContentRuleset(self, id,rulesetID):
        return self._connection.delete(url='/collections/' + str(id))+'/rulesets/'+str(rulesetID)




