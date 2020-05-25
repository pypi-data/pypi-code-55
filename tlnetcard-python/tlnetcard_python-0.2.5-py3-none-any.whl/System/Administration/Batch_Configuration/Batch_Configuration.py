# Batch_Configuration.py
# Ethan Guthrie
# 04/14/2020
# Allows batch configurations for SNMP or system settings to be uploaded or downloaded.

from os.path import isfile
from pathlib import Path
from platform import system
from requests_html import HTMLSession
from urllib3.exceptions import InsecureRequestWarning
from warnings import filterwarnings

class Batch_Configuration:
    # Initializes the Batch_Configuration object.
    def __init__(self, login_object):
        self._login_object = login_object
        self._post_url = login_object.getBaseURL() + "/delta/adm_batch"
    # Downloads the SNMP configuration and saves it to the specified file.
    def downloadSNMPConfiguration(self, path=None):
        # Setting path to downloads directory for operating system if no path was specified.
        if path is None:
            path = str(Path.home())
            if system() == "Windows":
                path += "\\Downloads\\snmp_config.ini"
            else:
                path += "/Downloads/snmp_config.ini"

        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)

        # Creating download payload.
        download_data = {
            'DL_SNMP': 'Download'
        }

        # Submitting download request and writing to file.
        with open(path, "w") as outFile:
            outFile.write(self._login_object.getSession().post(self._post_url, data=download_data, verify=self._login_object.getRejectInvalidCerts()).text)

        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return
    # Downloads the system configuration and saves it to the specified file.
    def downloadSystemConfiguration(self, path=None):
        # Setting path to downloads directory for operating system if no path was specified.
        if path is None:
            path = str(Path.home())
            if system() == "Windows":
                path += "\\Downloads\\system_config.ini"
            else:
                path += "/Downloads/system_config.ini"
        
        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)

        # Creating download payload.
        download_data = {
            'DL_SYSTEM': 'Download'
        }

        # Submitting download request and writing to file.
        with open(path, "w") as outFile:
            outFile.write(self._login_object.getSession().post(self._post_url, data=download_data, verify=self._login_object.getRejectInvalidCerts()).text)

        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return
    # Uploads the specified SNMP configuration file.
    def uploadSNMPConfiguration(self, path="snmp_config.ini"):
        # Testing if the file specified in path exists.
        if not isfile(path):
            print("Specified configuration file does not exist!")
            return -1

        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)

        # Creating upload payload.
        upload_data = {
            'UL_F_SNMP': path,
            'UL_SNMP': 'Upload'
        }

        # Uploading SNMP configuration.
        self._login_object.getSession().post(self._post_url, data=upload_data, verify=self._login_object.getRejectInvalidCerts())
        print("NOTE: The card at " + self._login_object.getBaseURL() + " will be offline for approximately 10 seconds.")

        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return
    # Uploads the specified system configuration file.
    def uploadSystemConfiguration(self, path="system_config.ini"):
        # Testing if the file specified in path exists.
        if not isfile(path):
            print("Specified configuration file does not exist!")
            return -1

        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)

        # Creating upload payload.
        upload_data = {
            'UL_F_SYSTEM': path,
            'UL_SYSTEM': 'Upload'
        }

        # Uploading system configuration.
        self._login_object.getSession().post(self._post_url, data=upload_data, verify=self._login_object.getRejectInvalidCerts())
        print("NOTE: The card at " + self._login_object.getBaseURL() + " will be offline for approximately 10 seconds.")

        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return