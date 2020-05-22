# ftp.py
# Ethan Guthrie
# 05/01/2020
""" Allows FTP settings to be configured. """

class Ftp:
    """ Class for the Ftp object. """
    def __init__(self, login_object):
        """ Initialize Ftp object. """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/adm_ftp.asp"
        self._post_url = login_object.get_base_url() + "/delta/adm_ftp"
    def disable_ftp(self):
        """ Disables FTP. """
        # Generating payload.
        ftp_data = {
            "FTP_FTP": "0",
        }

        # Uploading time server configuration.
        self._login_object.get_session().post(self._post_url, data=ftp_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def enable_ftp(self):
        """ Enables FTP. """
        # Generating payload.
        ftp_data = {
            "FTP_FTP": "1",
        }

        # Uploading time server configuration.
        self._login_object.get_session().post(self._post_url, data=ftp_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def get_ftp_port(self):
        """ GETs the port in use for FTP. """
        # GETing FTP page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for primary server.
        addr = resp.text.find("NAME=\"FTP_PORT_FTP\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)

        return int(resp.text[start_index:end_index])
    def set_ftp_port(self, port=21):
        """ Sets the port for use by FTP. """
        # Generating payload.
        ftp_data = {
            "FTP_FTP": "1",
            "FTP_PORT_FTP": str(port),
        }

        # Uploading time server configuration.
        self._login_object.get_session().post(self._post_url, data=ftp_data,
                                              verify=self._login_object.get_reject_invalid_certs())
