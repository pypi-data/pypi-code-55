import os
import sys
import json
import base64
import requests
import hashlib

from .domain import FlowName, JobBuildNumber, AgentToken, Job, ServerUrl, AgentJobDir

HttpHeaderWithJson = {
    "Content-Type": "application/json",
    "AGENT-TOKEN": AgentToken
}

HttpHeaders = {
    "AGENT-TOKEN": AgentToken
}


def GetVar(name, required=True):
    val = os.environ.get(name)
    if required and val is None:
        sys.exit("{} is missing".format(name))
    return val


def GetCurrentJob():
    return Job()


def ToBase64String(strVal):
    b64bytes = base64.b64encode(strVal.encode("utf-8"))
    return str(b64bytes, 'utf-8')


def FindFiles(file, path=AgentJobDir):
    files = []

    for i in os.listdir(path):
        fullPath = os.path.join(path, i)

        if os.path.isdir(fullPath) and not i.startswith("."):
            files += FindFiles(file, fullPath)

        if os.path.isfile(fullPath) and i == file:
            files.append(fullPath)

    return files


def MD5(path):
    md5Hash = hashlib.md5()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            md5Hash.update(byte_block)
        return md5Hash.hexdigest()


class Client:
    def __init__(self):
        pass

    def getCredential(self, name):
        try:
            url = "{}/api/secret/{}".format(ServerUrl, name)
            r = requests.get(url=url, headers=HttpHeaderWithJson)
            if r.status_code is 200:
                body = r.text
                return json.loads(body)

            return None
        except Exception as e:
            print(e)
            return None

    def getConfig(self, name):
        try:
            url = "{}/api/config/{}".format(ServerUrl, name)
            r = requests.get(url=url, headers=HttpHeaderWithJson)
            if r.status_code is 200:
                body = r.text
                return json.loads(body)

            return None
        except Exception as e:
            print(e)
            return None


    def listFlowUsers(self):
        try:
            url = "{}/api/flow/{}/users".format(ServerUrl, FlowName)
            r = requests.get(url=url, headers=HttpHeaderWithJson)

            if r.status_code is 200:
                body = r.text
                return json.loads(body)

            return None
        except Exception as e:
            print(e)
            return None

    def sendJobReport(self, path, name, zipped, contentType, entryFile=""):
        try:
            url = "{}/api/flow/{}/job/{}/report".format(
                ServerUrl, FlowName, JobBuildNumber)

            body = {
                "name": name,
                "zipped": zipped,
                "type": contentType,
                "entryFile": entryFile
            }

            r = requests.post(url=url, headers=HttpHeaders, files={
                'file': open(path, 'rb'),
                'body': ('', json.dumps(body), 'application/json')
            })
            return r.status_code
        except Exception as e:
            print(e)
            return -1

    def uploadJobArtifact(self, path, srcDir=None):
        try:
            url = "{}/api/flow/{}/job/{}/artifact".format(
                ServerUrl, FlowName, JobBuildNumber)

            body = {
                "md5": MD5(path)
            }

            if srcDir != None:
                body["srcDir"] = srcDir

            r = requests.post(url=url, headers=HttpHeaders, files={
                'file': open(path, 'rb'),
                "body": ('', json.dumps(body), 'application/json')
            })

            return r.status_code
        except Exception as e:
            print(e)
            return -1

    def sendStatistic(self, body):
        try:
            url = "{}/api/flow/{}/stats".format(ServerUrl, FlowName)
            r = requests.post(
                url=url, headers=HttpHeaderWithJson, data=json.dumps(body))
            return r.status_code
        except Exception as e:
            print(e)
            return -1

    def addJobContext(self, var):
        try:
            url = "{}/api/flow/{}/job/{}/context".format(
                ServerUrl, FlowName, JobBuildNumber)
            r = requests.post(url=url, headers=HttpHeaderWithJson,
                              data=json.dumps(var))
            return r.status_code
        except Exception as e:
            print(e)
            return -1
