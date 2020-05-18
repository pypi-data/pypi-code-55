#  Copyright (c) 2020 Netflix.
#  All rights reserved.
import json
import re
from typing import Dict

# Implementation libs
from ntscli_cloud_lib import host_to_rae_name
from ntscli_cloud_lib.log import logger


def is_rae_name_pattern(userstring):
    pattern = r"^r\d{7}$"
    foundparts = re.findall(pattern, userstring)
    if len(foundparts) == 1:
        return True
    else:
        return False


class DeviceIdentifier:
    """
    Identify a device to the mqtt-router service and Automator module.

    The required key "rae" indicates:
    * the RAE/Automator pair to route the MQTT message to
    * the RAE/Network Agent/Registry to scope the rest of the identifier in
    """

    def __init__(self, **kwargs):
        """Constructor."""
        self.esn = kwargs["esn"] if "esn" in kwargs else None
        self.ip = kwargs["ip"] if "ip" in kwargs else None
        self.serial = kwargs["serial"] if "serial" in kwargs else None
        self.rae = host_to_rae_name(kwargs["rae"]) if "rae" in kwargs else None

    def as_dict(self) -> Dict:
        """
        Get the dict representation of this identifier.

        If there is no valid value set, raise a ValueError.
        :return:
        """
        result = {"target": {}}
        if self.esn is not None:
            result["target"].update({"esn": self.esn})

        if self.ip is not None:
            result["target"].update({"ip": self.ip})

        if self.serial is not None:
            result["target"].update({"serial": self.serial})

        if len(result["target"].keys()) < 1:
            raise ValueError("No device identifier was set.")

        if self.rae is not None:
            result["target"].update({"rae": self.rae})

        return result

    def as_json(self) -> str:
        """
        Get the json serialized representation of this as a string.

        This is generally deprecated in favor of as_dict.

        :return:
        """
        return json.dumps(self.as_dict())

    @staticmethod
    def sanity_check(id_: Dict) -> bool:
        """
        Perform a basic sanity check on a dict to see if it contains an identifier.

        Note that the value of the identifier is not checked, even for formatting.

        :param id_:
        :return:
        """
        valid = "target" in id_ and ("esn" in id_["target"] or "ip" in id_["target"] or "serial" in id_["target"])

        if valid:
            valid = "rae" not in id_["target"] or ("rae" in id_["target"] and is_rae_name_pattern(id_["target"]["rae"]))

        if not valid:
            logger.error("The device identifier is in the wrong format.")
            logger.error(
                "A device identifier is a JSON object stored at the key 'target', with one or more of the keys 'esn', 'ip', 'rae', and 'serial':"
            )
            logger.error('{"target": {"esn": "NFANDROID...", "ip": "192...", "rae": "r3000100"}, ...')

            logger.error(
                "The rae can be looked up if the ESN is provided. The device registry will try to resolve other combinations if it can."
            )

        return valid
