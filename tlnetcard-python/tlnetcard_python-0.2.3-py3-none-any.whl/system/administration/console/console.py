# console.py
# Ethan Guthrie
# 05/04/2020
""" Allows for console settings to be configured. """

# Standard library.
from os.path import isfile

class Console:
    """ Class for the Console object. """
    def __init__(self, login_object):
        """ Initializes the Console object. """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/adm_console.asp"
        self._post_url = login_object.get_base_url() + "/delta/adm_console"
    def disable_ssh(self):
        """ Disables SSH. """
        # Generating payload.
        console_data = {
            "CON_SSH": "0"
        }

        # Uploading console configuration.
        self._login_object.get_session().post(self._post_url, data=console_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def disable_telnet(self):
        """ Disables Telnet. """
        # Generating payload.
        console_data = {
            "CON_TELNET": "0"
        }

        # Uploading console configuration.
        self._login_object.get_session().post(self._post_url, data=console_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def enable_ssh(self):
        """ Enables SSH. """
        # Generating payload.
        console_data = {
            "CON_SSH": "1"
        }

        # Uploading console configuration.
        self._login_object.get_session().post(self._post_url, data=console_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def enable_telnet(self):
        """ Enables Telnet. """
        # Generating payload.
        console_data = {
            "CON_TELNET": "1"
        }

        # Uploading console configuration.
        self._login_object.get_session().post(self._post_url, data=console_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def get_ssh_port(self):
        """ GETs the port in use for SSH. """
        # GETing Console page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for SSH Port.
        addr = resp.text.find("NAME=\"CON_PORT_SSH\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)

        return int(resp.text[start_index:end_index])
    def get_telnet_port(self):
        """ GETs the port in use for Telnet. """
        # GETing Console page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for Telnet Port.
        addr = resp.text.find("NAME=\"CON_PORT_TELNET\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)

        return int(resp.text[start_index:end_index])
    def set_ssh_port(self, port=22):
        """ Sets the port for use by SSH. """
        # Generating payload.
        console_data = {
            "CON_SSH": "1",
            "CON_PORT_SSH": str(port)
        }

        # Uploading console configuration.
        self._login_object.get_session().post(self._post_url, data=console_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def set_telnet_port(self, port=23):
        """ Sets the port for use by Telnet. """
        # Generating payload.
        console_data = {
            "CON_TELNET": "1",
            "CON_PORT_TELNET": str(port)
        }

        # Uploading console configuration.
        self._login_object.get_session().post(self._post_url, data=console_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def upload_auth_public_key(self, key):
        """ Uploads the provided authentication public key. """
        # Testing if the file specified in path exists.
        if not isfile(key):
            print("Specified key file does not exist!")
            return -1

        # Generating payload.
        console_data = {
            "CON_PUB": key
        }

        self._login_object.get_session().post(self._post_url, data=console_data,
                                              verify=self._login_object.get_reject_invalid_certs())
        return 0
    def upload_dsa_host_key(self, key):
        """ Uploads the provided DSA host key. """
        # Testing if the file specified in path exists.
        if not isfile(key):
            print("Specified key file does not exist!")
            return -1

        # Generating payload.
        console_data = {
            "CON_DSA": key
        }

        self._login_object.get_session().post(self._post_url, data=console_data,
                                              verify=self._login_object.get_reject_invalid_certs())
        return 0
    def upload_rsa_host_key(self, key):
        """ Uploads the provided RSA host key. """
        # Testing if the file specified in path exists.
        if not isfile(key):
            print("Specified key file does not exist!")
            return -1

        # Generating payload.
        console_data = {
            "CON_RSA": key
        }

        self._login_object.get_session().post(self._post_url, data=console_data,
                                              verify=self._login_object.get_reject_invalid_certs())
        return 0
