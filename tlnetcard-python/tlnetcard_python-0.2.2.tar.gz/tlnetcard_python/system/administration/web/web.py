# web.py
# Ethan Guthrie
# 05/04/2020
""" Allows web host settings to be configured. """

# Standard library.
from os.path import isfile

class Web:
    """ Class for the Web object. """
    def __init__(self, login_object):
        """ Initializes the Web object. """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/adm_web.asp"
        self._post_url = login_object.get_base_url() + "/delta/adm_web"
    def disable_http(self):
        """ Disables HTTP access. """
        # Generating payload.
        web_data = {
            "WEB_HTTP": "0"
        }

        # Uploading web configuration.
        self._login_object.get_session().post(self._post_url, data=web_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def disable_https(self):
        """ Disables HTTPS access. """
        # Generating payload.
        web_data = {
            "WEB_HTTPS": "0"
        }

        # Uploading web configuration.
        self._login_object.get_session().post(self._post_url, data=web_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def enable_http(self):
        """ Enables HTTP access. """
        # Generating payload.
        web_data = {
            "WEB_HTTP": "1"
        }

        # Uploading web configuration.
        self._login_object.get_session().post(self._post_url, data=web_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def enable_https(self):
        """ Enables HTTPS access. """
        # Generating payload.
        web_data = {
            "WEB_HTTPS": "1"
        }

        # Uploading web configuration.
        self._login_object.get_session().post(self._post_url, data=web_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def get_http_port(self):
        """ GETs the port in use for HTTP. """
        # GETing Web page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for HTTP Port.
        addr = resp.text.find("NAME=\"WEB_PORT_HTTP\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)

        return int(resp.text[start_index:end_index])
    def get_https_port(self):
        """ GETs the port in use for HTTPS. """
        # GETing Web page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for HTTP Port.
        addr = resp.text.find("NAME=\"WEB_PORT_HTTPS\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)

        return int(resp.text[start_index:end_index])
    def get_web_refresh(self):
        """ GETs the web refresh time in seconds. """
        # GETing Web page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for web refresh.
        addr = resp.text.find("NAME=\"WEB_REFRESH\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)

        return int(resp.text[start_index:end_index])
    def set_http_port(self, port=80):
        """ Sets the port for use by HTTP. """
        # Generating payload.
        web_data = {
            "WEB_HTTP": "1",
            "WEB_PORT_HTTP": str(port)
        }

        # Uploading web configuration.
        self._login_object.get_session().post(self._post_url, data=web_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def set_https_port(self, port=443):
        """ Sets the port for use by HTTPS. """
        # Generating payload.
        web_data = {
            "WEB_HTTPS": "1",
            "WEB_PORT_HTTPS": str(port)
        }

        # Uploading web configuration.
        self._login_object.get_session().post(self._post_url, data=web_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def set_web_refresh(self, seconds=10):
        """ Sets the web refresh time to ```seconds``` seconds. """
        # Generating payload.
        web_data = {
            "WEB_REFRESH": str(seconds)
        }

        # Uploading web configuration.
        self._login_object.get_session().post(self._post_url, data=web_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def upload_ssl_cert(self, path):
        """ Uploads the provided SSL certificate. """
        # Testing if the file specified in path exists.
        if not isfile(path):
            print("Specified PEM file does not exist!")
            return -1

        # Generating payload.
        web_data = {
            "WEB_SSLCERT": path
        }

        # Uploading web configuration.
        self._login_object.get_session().post(self._post_url, data=web_data,
                                              verify=self._login_object.get_reject_invalid_certs())
        return 0
