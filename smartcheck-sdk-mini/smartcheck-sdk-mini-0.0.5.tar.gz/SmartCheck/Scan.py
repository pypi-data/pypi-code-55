#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class Scans:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##Sessions
    def list(self, limit=25, expand="all", registry=None, repository=None, tag=None, digest=None, exact=None, status=None):
        params={'limit': limit, 'expand':expand}
        if registry:
            params['registry'] = registry
        if repository:
            params['repository'] = repository
        if tag:
            params['tag'] = tag
        if digest:
            params['digest'] = digest
        if exact:
            params['exact'] = exact
        if status:
            params['status'] = status
        rtv = self._connection.get(url='/scans', params=params)
        items = rtv['scans']
        while "next" in rtv:
            params['cursor']= rtv['next']
            rtv = self._connection.get(url='/scans', params=params)
            items.extend(rtv['scans'])
        return items
    def create(self, payload):
        return self._connection.post(url='/scans', data=payload)
    def describe(self, id, expand="all"):
        params = {'expand': expand}
        return self._connection.get(url='/scans/' + str(id), params=params )
    def describeScanMetrics(self):
        return self._connection.get(url='/scans/metrics' )
    def cancel(self, id):
        return self._connection.delete(url='/sessions/' + str(id))

    def listLayerMalwareFindingsScans(self, id, layer, limit=25, expand="all"):
            params = {'limit': limit, 'expand': expand}
            rtv = self._connection.get(url='/scans/'+str(id)+"/layers/"+str(layer)+"/malware", params=params)
            items = rtv['malware']
            while "next" in rtv:
                params['cursor']=rtv['next']
                rtv = self._connection.get(url='/scans/'+str(id)+"/layers/"+str(layer)+"/malware", params=params)
                items.extend(rtv['malware'])
            return items
    def listLayerVulnerabilityFindingsScans(self, id, layer, limit=25, expand="all", severity=None):
            params = {'limit': limit, 'expand': expand}
            if severity:
                params['severity'] = severity
            rtv = self._connection.get(url='/scans/'+str(id)+"/layers/"+str(layer)+"/vulnerabilities", params=params)
            items = rtv['vulnerabilities']
            while "next" in rtv:
                params['cursor']=rtv['next']
                rtv = self._connection.get(url='/scans/'+str(id)+"/layers/"+str(layer)+"/vulnerabilities", params=params)
                items.extend(rtv['vulnerabilities'])
            return items
    def listLayerContentFindingsScans(self, id, layer, limit=25, expand="all", severity=None):
            params = {'limit': limit, 'expand': expand}
            if severity:
                params['severity'] = severity
            rtv = self._connection.get(url='/scans/'+str(id)+"/layers/"+str(layer)+"/contents", params=params)
            items = rtv['contents']
            while "next" in rtv:
                params['cursor']=rtv['next']
                rtv = self._connection.get(url='/scans/'+str(id)+"/layers/"+str(layer)+"/contents", params=params)
                items.extend(rtv['contents'])
            return items
    def listLayerContentFindingsScans(self, id, layer, limit=25, expand="all", severity=None):
            params = {'limit': limit, 'expand': expand}
            if severity:
                params['severity'] = severity
            rtv = self._connection.get(url='/scans/'+str(id)+"/layers/"+str(layer)+"/contents", params=params)
            items = rtv['contents']
            while "next" in rtv:
                params['cursor']=rtv['next']
                rtv = self._connection.get(url='/scans/'+str(id)+"/layers/"+str(layer)+"/contents", params=params)
                items.extend(rtv['contents'])
            return items

    def listScanChecklist(self, id, limit=25, expand="all"):
        params = {'limit': limit, 'expand': expand}
        rtv = self._connection.get(url='/scans/' + str(id) + "/checklists", params=params)
        items = rtv['checklists']
        while "next" in rtv:
            params['cursor'] = rtv['next']
            rtv = self._connection.get(url='/scans/' + str(id) + "/checklists", params=params)
            items.extend(rtv['checklists'])
        return items
    def describeConfigurationChecklist(self, ScanID, cheklistID, expand="all"):
        params = {'expand': expand}
        return self._connection.get(url='/scans/' + str(ScanID) + '/checklists/'+str(cheklistID), params=params )
    def listConfigurationChecklistProfileRules(self, ScanID, cheklistID, profileID):
        return self._connection.get(url='/scans/' + str(ScanID) + '/checklists/'+str(cheklistID) +"profiles/" +str(profileID)+ "/rules" )


