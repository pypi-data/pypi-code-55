# batch_configuration.py
# Ethan Guthrie
# 04/14/2020
""" Allows batch configurations for SNMP or system settings to be uploaded or downloaded. """

# Standard library.
from os.path import isfile
from pathlib import Path
from platform import system

class BatchConfiguration:
    """ Class for the BatchConfiguration object. """
    def __init__(self, login_object):
        """ Initializes the BatchConfiguration object. """
        self._login_object = login_object
        self._post_url = login_object.get_base_url() + "/delta/adm_batch"
    def download_snmp_configuration(self, path=None):
        """ Downloads the SNMP configuration and saves it to the specified file. """
        # Setting path to downloads directory for operating system if no path was specified.
        if path is None:
            path = str(Path.home())
            if system() == "Windows":
                path += "\\Downloads\\snmp_config.ini"
            else:
                path += "/Downloads/snmp_config.ini"

        # Creating download payload.
        download_data = {
            'DL_SNMP': 'Download'
        }

        # Submitting download request and writing to file.
        verify = self._login_object.get_reject_invalid_certs()
        with open(path, "w") as out_file:
            out_file.write(self._login_object.get_session().post(self._post_url, data=download_data,
                                                                 verify=verify).text)
    def download_system_configuration(self, path=None):
        """ Downloads the system configuration and saves it to the specified file. """
        # Setting path to downloads directory for operating system if no path was specified.
        if path is None:
            path = str(Path.home())
            if system() == "Windows":
                path += "\\Downloads\\system_config.ini"
            else:
                path += "/Downloads/system_config.ini"

        # Creating download payload.
        download_data = {
            'DL_SYSTEM': 'Download'
        }

        # Submitting download request and writing to file.
        verify = self._login_object.get_reject_invalid_certs()
        with open(path, "w") as out_file:
            out_file.write(self._login_object.get_session().post(self._post_url, data=download_data,
                                                                 verify=verify).text)
    def upload_snmp_configuration(self, path="snmp_config.ini"):
        """ Uploads the specified SNMP configuration file. """
        # Testing if the file specified in path exists.
        if not isfile(path):
            print("Specified configuration file does not exist!")
            return -1

        # Creating upload payload.
        upload_data = {
            'UL_SNMP': 'Upload'
        }
        upload_file = {
            'UL_F_SNMP': (path.split("/")[-1], open(path, 'rb'), 'multipart/form-data'),
        }

        # Uploading SNMP configuration.
        self._login_object.get_session().post(self._post_url, data=upload_data, files=upload_file,
                                              verify=self._login_object.get_reject_invalid_certs())
        print("NOTE: The card at " + self._login_object.get_base_url()
              + " will be offline for approximately 10 seconds.")

        return 0
    def upload_system_configuration(self, path="system_config.ini"):
        """ Uploads the specified system configuration file. """
        # Testing if the file specified in path exists.
        if not isfile(path):
            print("Specified configuration file does not exist!")
            return -1

        # Creating upload payload.
        upload_data = {
            'UL_SYSTEM': 'Upload'
        }
        upload_file = {
            'UL_F_SYSTEM': (path.split("/")[-1], open(path, 'rb'), 'multipart/form-data'),
        }

        # Uploading system configuration.
        self._login_object.get_session().post(self._post_url, data=upload_data, files=upload_file,
                                              verify=self._login_object.get_reject_invalid_certs())
        print("NOTE: The card at " + self._login_object.get_base_url()
              + " will be offline for approximately 10 seconds.")

        return 0
