#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class Overrides:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection

    def listVulnerabilityFindingOverrides(self, limit=25, query=None):
        url = "/overrides/vulnerabilities"
        params={'limit': limit}
        if query:
            params['query'] = query
        rtv = self._connection.get(url=url, params=params)
        items = rtv['overrides']
        while "next" in rtv:
            params['cursor'] = rtv['next']
            rtv = self._connection.get(url=url, params=params)
            items.extend(rtv['overrides'])
        return items
    def createVulnerabilityFindingOverride(self, payload):
        return self._connection.post(url='/overrides/vulnerabilities', data=payload)
    def describeVulnerabilityFindingOverride(self, id):
        return self._connection.get(url='/overrides/vulnerabilities/' + str(id))
    def modifyVulnerabilityFindingOverride(self, id, payload):
        return self._connection.post(url='/overrides/vulnerabilities/' + str(id), data=payload)
    def deleteVulnerabilityFindingOverride(self, id):
        return self._connection.delete(url='/overrides/vulnerabilities/' + str(id))
    def listContentFindingOverrides(self, limit=25, query=None):
        url = "/overrides/contents"
        params={'limit': limit}
        if query:
            params['query'] = query
        rtv = self._connection.get(url=url, params=params)
        items = rtv['overrides']
        while "next" in rtv:
            params['cursor'] = rtv['next']
            rtv = self._connection.get(url=url, params=params)
            items.extend(rtv['overrides'])
        return items
    def createContentFindingOverride(self, payload):
        return self._connection.post(url='/overrides/contents', data=payload)
    def describeContentFindingOverride(self, id):
        return self._connection.get(url='/overrides/contents/' + str(id))
    def modifyContentFindingOverride(self, id, payload):
        return self._connection.post(url='/overrides/contents' + str(id), data=payload)
    def deleteContentFindingOverride(self, id):
        return self._connection.delete(url='/overrides/contents' + str(id))
    def listChecklistFindingOverrides(self, limit=25, query=None):
        url = "/overrides/checklists"
        params={'limit': limit}
        if query:
            params['query'] = query
        rtv = self._connection.get(url=url, params=params)
        items = rtv['overrides']
        while "next" in rtv:
            params['cursor'] = rtv['next']
            rtv = self._connection.get(url=url, params=params)
            items.extend(rtv['overrides'])
        return items
    def createChecklistFindingOverride(self, payload):
        return self._connection.post(url='/overrides/checklists', data=payload)
    def describeChecklistFindingOverride(self, id):
        return self._connection.get(url='/overrides/checklists/' + str(id))
    def modifyChecklistFindingOverride(self, id, payload):
        return self._connection.post(url='/overrides/checklists' + str(id), data=payload)
    def deleteChecklistFindingOverride(self, id):
        return self._connection.delete(url='/overrides/checklists' + str(id))




