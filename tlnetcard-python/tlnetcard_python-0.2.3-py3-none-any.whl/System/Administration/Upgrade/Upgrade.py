# Upgrade.py
# Ethan Guthrie
# 04/16/2020
# Allows SNMP Device Firmware to be upgraded.

from os.path import isfile
from requests_html import HTMLSession
from urllib3.exceptions import InsecureRequestWarning
from warnings import filterwarnings

class Upgrade:
    # Initializes the Upgrade object.
    def __init__(self, login_object):
        self._login_object = login_object
        self._post_url = login_object.getBaseURL() + "/delta/adm_upgrade"
    # Upgrades SNMP Device Firmware.
    def upgradeSNMPFirmware(self, path="ups-tl-01_12_05c.bin"):
        # Testing if the file specified in path exists.
        if not isfile(path):
            print("Specified configuration file does not exist!")
            return -1

        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)

        # Creating upload payload.
        upgrade_data = {
            'UL_F_NETWORK': path
        }

        # Uploading SNMP configuration.
        self._login_object.getSession().post(self._post_url, data=upgrade_data, verify=self._login_object.getRejectInvalidCerts())
        print("NOTE: The card at " + self._login_object.getBaseURL() + " will be offline for approximately 1 minute.")

        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return