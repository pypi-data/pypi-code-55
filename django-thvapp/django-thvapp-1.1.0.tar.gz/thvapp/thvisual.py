import hashlib
import time
import requests

class THVClient:
    def __init__(self, appid, appkey, server, cluster, user, timeout=60):
        self.appid = appid
        self.appkey = appkey
        self.server = server
        self.cluster = cluster
        self.user = user
        self.timeout = timeout

    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    def _make_sig(self, timestamp, vapp=None):
        str1 = "appkey=%s&timestamp=%s&cluster=%s&user=%s" % (
            self.appkey, timestamp, self.cluster, self.user)

        if vapp is not None:
            str1 = str1 + "&vapp=" + vapp

        hashStr = hashlib.sha256()
        hashStr.update(str1.encode())
        sig = hashStr.hexdigest()
        return sig

    def listApps(self):
        url = "%s/v1/%s/%s/visual/list?appid=%s" % (self.server, self.cluster, self.user, self.appid)
        # print(url)
        timestamp = int(time.time())
        data = {
            "sig": self._make_sig(timestamp),
            "timestamp": timestamp,
        }

        resp = requests.post(url=url, data=data, timeout=self.timeout)

        if resp.status_code < 300:
            # print(resp.json())
            return resp.json()
        else:
            # print(resp.json())
            raise ValueError(resp.text)

    def launchApp(self, vapp,gpu=0,version="",winWidth=1920,winHeight=1200,param="",client="w"):
        if vapp == "shell":
            url = "%s/v1/%s/%s/web/shell/launch?appid=%s" % (self.server, self.cluster, self.user, self.appid)
            timestamp = int(time.time())
            data = {
                "sig": self._make_sig(timestamp),
                "timestamp": timestamp,
            }
        else:
            url = "%s/v1/%s/%s/visual/%s/launch?appid=%s" % (self.server, self.cluster, self.user, vapp, self.appid)
            # print(url)
            timestamp = int(time.time())
            data = {
                "sig": self._make_sig(timestamp, vapp),
                "timestamp": timestamp,
            }
            if param != "":
                data["param"] = param
            if int(gpu) == 1:
                data["gpu"] = "true"
            data["client"] = client
            data["version"] = version
            if not self.is_number(winWidth):
                winWidth = 1920
            if not self.is_number(winHeight):
                winHeight = 1200
            resolution = "{winw}x{winh}".format(winw=winWidth, winh=winHeight)
            data["resolution"] = resolution

        resp = requests.post(url=url, data=data, timeout=self.timeout)

        if resp.status_code < 300:
            resJ = resp.json()
            return resJ
        else:
            # print(resp.text)
            raise ValueError(resp.text)

    def closeApp(self,vapp,gpu=0,version="",param="",client="w"):
        if vapp == "shell":
            return {"status":False,"error":"shell app not allowed close!!"}
        else:
            url = "%s/v1/%s/%s/visual/%s/close?appid=%s" % (self.server, self.cluster, self.user, vapp, self.appid)
            timestamp = int(time.time())
            data = {
                "sig": self._make_sig(timestamp, vapp),
                "timestamp": timestamp,
            }
            if param != "":
                data["param"] = param
            if int(gpu) == 1:
                data["gpu"] = "true"
            data["client"] = client
            data["version"] = version
            # print(data)

        resp = requests.post(url=url, data=data, timeout=self.timeout)

        if resp.status_code < 300:
            return {"status":True}
        else:
            raise ValueError(resp.text)