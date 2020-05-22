# information.py
# Ethan Guthrie
# 05/13/2020
""" Allows the firmware version for the TLNETCARD to be retreived. """

class Information:
    """ Class for the Information object. """
    def __init__(self, login_object):
        """ Initializes the BatchConfiguration object. """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/ups/about_info.asp"
    def get_firmware_version(self):
        """ GETs the current firmware version. """
        # GETing Information page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for firmware version.
        start_index = str(resp.text).find("Version : ") + 10
        end_index = str(resp.text).find("\n", start_index)
        return resp.text[start_index:end_index]
