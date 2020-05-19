# syslog.py
# Ethan Guthrie
# 04/16/2020
""" Allows syslog servers to be added or removed. """

class Syslog:
    """ Class for the syslog object. """
    def __init__(self, login_object):
        """ Initializes the Syslog object. """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/adm_syslog.asp"
        self._post_url = login_object.get_base_url() + "/delta/adm_syslog"
    def add_server(self, server):
        """ Adds a syslog server. """
        # Quitting if four servers are already listed.
        curr_servers = self.get_servers()
        if len(curr_servers) >= 4:
            return -1

        # Returning success if server is already in use.
        if server in curr_servers:
            return 0

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
        self._login_object.get_session().post(self._post_url, data=syslog_data,
                                              verify=self._login_object.get_reject_invalid_certs())

        return 0
    def clear_servers(self):
        """ Clears all syslog servers. """
        # Generating payload.
        syslog_data = {}
        for i in range(0, 4):
            syslog_data["SLG_SERVER" + str(i + 1)] = ""

        # Uploading server configuration.
        self._login_object.get_session().post(self._post_url, data=syslog_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def disable_syslog(self):
        """ Disables syslog servers. """
        # Generating payload.
        syslog_data = {
            'SLG_SLG': 0
        }

        # Uploading server configuration.
        self._login_object.get_session().post(self._post_url, data=syslog_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def enable_syslog(self):
        """ Enables syslog servers. """
        # Generating payload.
        syslog_data = {
            'SLG_SLG': 1
        }

        # Uploading server configuration.
        self._login_object.get_session().post(self._post_url, data=syslog_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def get_servers(self):
        """ GETs syslog servers and returns them in a list. """
        # GETing syslog page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for server names.
        servers = []
        inputs = resp.html.find("input")
        for i in inputs:
            is_server = str(i).find("SLG_SERVER")
            if is_server != -1:
                start_index = str(i).find("value=") + 7
                end_index = str(i).find("'", start_index)
                if str(i)[start_index:end_index]:
                    servers.append(str(i)[start_index:end_index])

        return servers
    def remove_server(self, server):
        """ Removes a syslog server. """
        # Quitting if server isn't listed.
        curr_servers = self.get_servers()
        if server not in curr_servers:
            return -1

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
        self._login_object.get_session().post(self._post_url, data=syslog_data,
                                              verify=self._login_object.get_reject_invalid_certs())
        return 0
