# Syslog.py
# Ethan Guthrie
# 04/16/2020
# Allows syslog servers to be added or removed.

from requests_html import HTMLSession
from urllib3.exceptions import InsecureRequestWarning
from warnings import filterwarnings

class Syslog:
    # Initializes the Syslog object.
    def __init__(self, login_object):
        self._login_object = login_object
        self._get_url = login_object.getBaseURL() + "/en/adm_syslog.asp"
        self._post_url = login_object.getBaseURL() + "/delta/adm_syslog"
    # Adds a syslog server.
    def addServer(self, server):
        # Quitting if four servers are already listed.
        curr_servers = self.getServers()
        if len(curr_servers) >= 4:
            return -1
        
        # Returning success if server is already in use.
        if server in curr_servers:
            return

        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)

        # Adding current servers to payload.
        syslog_data = {}
        i = 0   # Setting i to 0 here prevents error if curr_servers is empty.
        for i in range(0, len(curr_servers)):
            syslog_data["SLG_SERVER" + str(i + 1)] = curr_servers[i]
        
        # Adding new server to payload.
        syslog_data["SLG_SERVER" + str(i + 2)] = server

        # Adding empty server lines to payload.
        for j in range(i + 2, 4):
            syslog_data["SLG_SERVER" + str(j + 1)] = ""

        # Uploading server configuration.
        self._login_object.getSession().post(self._post_url, data=syslog_data, verify=self._login_object.getRejectInvalidCerts())
        
        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return
    # Clears all syslog servers.
    def clearServers(self):
        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)

        # Generating payload.
        syslog_data = {}
        for i in range(0, 4):
            syslog_data["SLG_SERVER" + str(i + 1)] = ""

        # Uploading server configuration.
        self._login_object.getSession().post(self._post_url, data=syslog_data, verify=self._login_object.getRejectInvalidCerts())
        
        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return
    # Disables syslog servers.
    def disableSyslog(self):
        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)

        # Generating payload.
        syslog_data = {
            'SLG_SLG': 0
        }

        # Uploading server configuration.
        self._login_object.getSession().post(self._post_url, data=syslog_data, verify=self._login_object.getRejectInvalidCerts())
        
        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return
    # Enables syslog servers.
    def enableSyslog(self):
        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)

        # Generating payload.
        syslog_data = {
            'SLG_SLG': 1
        }

        # Uploading server configuration.
        self._login_object.getSession().post(self._post_url, data=syslog_data, verify=self._login_object.getRejectInvalidCerts())
        
        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return
    # GETs syslog servers and returns them in a list.
    def getServers(self):
        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)

        # GETing syslog page.
        r = self._login_object.getSession().get(self._get_url)

        # Parsing response for server names.
        servers = []
        inputs = r.html.find("input")
        for i in inputs:
            is_server = str(i).find("SLG_SERVER")
            if is_server != -1:
                start_index = str(i).find("value=") + 7
                end_index = str(i).find("'", start_index)
                if str(i)[start_index:end_index]:
                    servers.append(str(i)[start_index:end_index])

        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return servers
    # Removes a syslog server.
    def removeServer(self, server):
        # Quitting if server isn't listed.
        curr_servers = self.getServers()
        if server not in curr_servers:
            return -1
        
        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)

        # Removing server from list.
        curr_servers.remove(server)

        # Adding remaining servers to payload.
        syslog_data = {}
        for i in range(0, len(curr_servers)):
            syslog_data["SLG_SERVER" + str(i + 1)] = curr_servers[i]

        # Adding empty server lines to payload.
        for j in range(i + 1, 4):
            syslog_data["SLG_SERVER" + str(j + 1)] = ""

        # Uploading server configuration.
        self._login_object.getSession().post(self._post_url, data=syslog_data, verify=self._login_object.getRejectInvalidCerts())
        
        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return