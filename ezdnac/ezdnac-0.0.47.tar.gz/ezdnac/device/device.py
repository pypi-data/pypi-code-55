from ezdnac.excepts import *
from ezdnac.utils import *
#import ezdnac.dnac
import requests
import json
import re
import os


# When initialized, populate device parameters:
# Retreive switchId based on serialnumber
class Device():
    def __init__(self, dnac, **kwargs):
        self.dnac = dnac
        self.id = None
        self.hostname = None
        self.serialNumber = None
        self.state = None
        self.deploymentId = None

        if 'id' in kwargs:
            self.id = kwargs['id']
            self.initMethod = 'id'
        elif 'sn' in kwargs:
            self.serialNumber = kwargs['sn']
            self.initMethod = 'sn'
        elif 'hostname' in kwargs:
            self.hostname = kwargs['hostname']
            self.initMethod = 'hostname'

        if self.id is None and self.serialNumber is None and self.hostname is None:
            raise ezDNACError(
                'No device argment found. Enter hostname, id or sn')

        # if init method is id, the device must be in inventory. Populate all attributes:
        if self.initMethod == 'id':
            try:
                self.state = "Provisioned"
                INVdevices = self.dnac.getInventoryDevies(id=self.id)
            except:
                raise ezDNACError('device not found by id')

        elif self.initMethod == 'hostname':
            try:
                INVdevices = self.dnac.getInventoryDevies(
                    hostname=self.hostname)
            except:
                raise ezDNACError('device not found by hostname')

        # if method is sn, the device can be either in inventory or pnp, have to try both
        elif self.initMethod == 'sn':
            INVdevices = self.dnac.getInventoryDevies(sn=self.serialNumber)

        else:
            return None

        self.state = "Provisioned"
        self.id = INVdevices['id']
        self.serialNumber = INVdevices['serialNumber']
        self.ip = INVdevices['managementIpAddress']
        self.hostname = INVdevices['hostname']
        self.platform = INVdevices['platformId']
        self.softwareVersion = INVdevices['softwareVersion']
        self.softwareType = INVdevices['softwareType']

        if self.state != "Provisioned" and self.initMethod == 'sn':
            try:
                # Otherwise try populate attributes via pnp:
                PNPdevices = self.dnac.getPnpDevices(sn=self.serialNumber)
                self.id = PNPdevices['id']
                self.state = PNPdevices['state']
                self.hostname = PNPdevices['name']
                self.platform = PNPdevices['pid']
                self.softwareVersion = PNPdevices['imageVersion']
                self.softwareType = PNPdevices['agentType']
            except:
                raise ezDNACError('device with serialNumber' +
                                  str(self.serialNumber) + ' not found')
            try:
                httpHeaders = PNPdevices['deviceInfo']['httpHeaders']
                for header in httpHeaders:
                    if header['key'] == 'clientAddress':
                        self.ip = header['value']
            except:
                pass

    def getInterfaces(self):
        endpoint = f"interface/network-device/{self.id}"
        data = restcall('GET', self.dnac, endpoint)
        return data

    def getTopology(self):
        ret = []
        endpoint = "topology/physical-topology/"
        data = restcall('GET', self.dnac, endpoint)
        connections = {}
        links = []
        for link in data['response']['links']:

            try:
                connections['sourcenode'] = link['source']
                connections['remotenode'] = link['target']
                connections['sourceif'] = link['startPortName']
                connections['remoteif'] = link['endPortName']
                links.append(dict(connections))
            except:
                pass
        ret = links
        return ret

    def getConnections(self):
        ret = []
        endpoint = "topology/physical-topology/"
        data = restcall('GET', self.dnac, endpoint)
        connections = {}
        links = []
        for link in data['response']['links']:
            try:
                if link['source'] == self.id:
                    connections['remotenode'] = link['target']
                    connections['remoteif'] = link['endPortName']
                    connections['localif'] = link['startPortName']
                    links.append(dict(connections))
                elif link['target'] == self.id:
                    connections['remotenode'] = link['source']
                    connections['remoteif'] = link['startPortName']
                    connections['localif'] = link['endPortName']
                    links.append(dict(connections))
            except:
                pass
        ret = links
        return ret

    def deployTemplate(self, template):
        """
        Inputs:
        template (obj) ezdnac template object

        Returns data (dict):
        {
        'deploymetId': id(str),   if error occurs, deploymentId returns None.
        'message': (str)
        }
        """
        data = {}
        data['deploymentId'] = None
        data['message'] = None
        endpoint = "template-programmer/template/deploy"

        payload = {
            "templateId": template.id,
            "targetInfo": [
                {
                    "id": self.id,
                    "type": "MANAGED_DEVICE_UUID",
                    "params": template.params
                }
            ]}

        response = restcall('POST', self.dnac, endpoint, jsondata=payload)


        # If error occurs, no id
        if 'response' in response and 'errorCode' in response['response']:
            data['deploymentId'] = None
            data['message'] = response['response']
            data['deployed'] = False
            return data

        # This is how the id should be found, if the API wasnt broken.
        if 'deploymentId' in response and type(response['deploymentId']) is int:
            data['deploymentId'] = response['deploymentId']
            data['message'] = 'Id found in response'
            data['deployed'] = True
            self.deploymentId = response
            return data

        # This is how it is solved with regex instead.
        if 'deploymentId' in response and type(response['deploymentId']) is not int:
            data['message'] = 'Id found with regex, broken response'

            # Testing if id is in response:
            resultRegex = (re.findall(r'Template Deployemnt Id.*', response['deploymentId']))

            if len(resultRegex) is not 0:
                Id = str(resultRegex).strip("['Template Deployemnt Id: ]")
                if resultRegex is not None:
                    data['deploymentId'] = Id
                    data['deployed'] = True
                    self.deploymentId = data
                    return data

        # If template was not deployed
        if re.match(r'.*already deployed with same params.*', response['deploymentId']):
            data['deploymentId'] = None
            data['deployed'] = True
            data['message'] = 'Same version already deployed with same params'
        else:
            data['deploymentId'] = None
            data['deployed'] = False
            data['message'] = 'Error'

        return data
 

    def deployTemplateStatus(self, **kwargs):
        if 'id' in kwargs:
            self.deploymentId = kwargs['id']

        if self.deploymentId == None:
            return None

        if self.deploymentId['deploymentId'] == None:
            return self.deploymentId['message']
        else:
            baseurl = "/dna/intent/api/v1/"
            endpoint = f"template-programmer/template/deploy/status/{self.deploymentId['deploymentId']}"
            data = restcall('GET', self.dnac, endpoint)

            if 'status' in data:
                return data['status']
            else:
                return data

    def deployTemplateReport(self, **kwargs):
        if 'id' in kwargs:
            self.deploymentId = kwargs['id']
        else:
            return None

        url = "https://" + self.dnac.ip + ":" + self.dnac.port + \
            "/dna/intent/api/v1/template-programmer/template/deploy/status/" + self.deploymentId
        payload = {}
        headers = {
            'x-auth-token': self.authToken,
            'Content-Type': 'application/json',
        }
        response = requests.request(
            "GET", url, headers=headers, json=payload, verify=verifySSL, timeout=timeout)

        data = json.loads(response.text)
        return data

    def findNextPortchannel(self):
        endpoint = f"interface/network-device/{self.id}"
        response = restcall('GET', self.dnac, endpoint)

        existing_ids = []
        for interface in response['response']:
            if re.match(r'Port-channel.*', str(interface['portName'])):
                intf = int(str(interface['portName']).strip("'Port-channel"))
                existing_ids.append(intf)

        for i in range(1, 49):
            if (i) not in existing_ids:
                next_id = i
                break
        return next_id

    def assignToSite(self, siteId):
        url = "https://" + self.dnac.ip + ":" + self.port + \
            "/dna/system/api/v1/site/" + siteId + "/device"
        payload = {
            "device": [
                {
                    "ip": self.ip
                }
            ]
        }

        headers = {
            'x-auth-token': self.authToken,
            'Content-Type': 'application/json',
            '__runsync': 'true',
            '__timeout': '10',
            '__persistbapioutput': 'true',
        }
        response = requests.request(
            "POST", url, headers=headers, json=payload, verify=verifySSL, timeout=timeout)
        #data = json.loads(response.text)
        return response.text

    def getNeighbors(self):
        connections = self.getConnections()
        neighbors = []
        for link in connections:
            if link['remotenode'] in neighbors:
                continue
            else:
                neighbors.append(link['remotenode'])
        return neighbors

    # return every interface connected to us from specific neighbor

    def getNeighborIfs(self, neighbor):
        connections = self.getConnections()
        interfaces = []
        for link in connections:
            if link['remotenode'] == neighbor:
                interfaces.append(link['remoteif'])
        return interfaces

    def getModules(self):
        endpoint = f'network-device/module?deviceId={self.id}'
        data = restcall('GET', self.dnac, endpoint)

        modules = data['modules']
        self.modules = modules

        switches = []
        for module in modules:
            name = module['name']
            switch = str((re.findall(r'Switch \d', name))).strip("[']")
            switches.append(switch)
        self.stackcount = len((set(switches)))

        return modules

    def claimDevice(self, siteId, **kwargs):
        endpoint = "onboarding/pnp-device/site-claim"
        try:
            payload = {
                "siteId": siteId,
                "deviceId": pnpDeviceId,
                "type": "Default",
                "imageInfo": {"imageId": "None", "skip": true},
                "configInfo": {"configId": kwargs['templateId'], "configParameters": [kwargs[params]]}
            }
        except:
            payload = {
                "siteId": siteId,
                "deviceId": self.id,
                "type": "Default",
                "imageInfo": {"imageId": "None", "skip": "true"},
                "configInfo": {"configId": "", "configParameters": []}
            }
        data = restcall('POST', self.dnac, endpoint, jsondata=payload)
        return data

    def sync(self):
        endpoint = 'network-device/sync'
        baseurl = '/dna/intent/api/v1/'
        payload = f'["{self.id}"]\n\n'
        data = restcall('PUT', self.dnac, endpoint, data=payload, baseurl=baseurl)

        self.taskId = data['response']['taskId']
        print(self.taskId)
        return data

    def getTaskStatus(self, **kwargs):
        if 'id' in kwargs:
            taskId = kwargs['id']
        elif self.taskId is not None:
            taskId = self.taskId
        else:
            return None

        endpoint = f'task/{self.taskId}'
        data = restcall('GET', self.dnac, endpoint)
        return data
