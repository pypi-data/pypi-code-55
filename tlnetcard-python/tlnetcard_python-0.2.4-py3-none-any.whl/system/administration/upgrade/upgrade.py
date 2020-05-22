# upgrade.py
# Ethan Guthrie
# 04/16/2020
""" Allows SNMP Device Firmware to be upgraded. """

# Standard library.
from os.path import isfile
# Required internal class.
from tlnetcard_python.monitor.about.information import Information

class Upgrade:
    """ Class for the Upgrade object. """
    def __init__(self, login_object):
        """ Initializes the Upgrade object. """
        self._login_object = login_object
        self._post_url = login_object.get_base_url() + "/delta/adm_upgrade"
        self._information_object = Information(self._login_object)
    def upgrade_snmp_firmware(self, path="ups-tl-01_12_05c.bin"):
        """ Upgrades SNMP Device Firmware. """
        # Testing if the file specified in path exists.
        if not isfile(path):
            print("Specified configuration file does not exist!")
            return -1

        # Creating upload payload.
        upgrade_data = {
            'UL_F_NETWORK': path
        }

        # Uploading SNMP configuration.
        self._login_object.get_session().post(self._post_url, data=upgrade_data,
                                              verify=self._login_object.get_reject_invalid_certs())
        print("NOTE: The card at " + self._login_object.get_base_url()
              + " will be offline for approximately 1 minute.")

        return 0
    def get_firmware_version(self):
        """ GETs the current firmware version. """
        return self._information_object.get_firmware_version()
