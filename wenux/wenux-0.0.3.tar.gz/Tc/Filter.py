import logging

from dataclasses import dataclass
from abc import abstractmethod

from Utils.Subprocess import check_call


class Filter(object):
    _priority = 0
    _flowid = ""
    @abstractmethod
    def _apply_filter(self):
        pass

    @staticmethod
    def generate_filters(filter_list):
        filter_strings = []
        filter_strings_ipv6 = []

        for tc_filter in filter_list:
            filter_tokens = tc_filter.split(",")

            try:
                filter_string = ""
                filter_string_ipv6 = ""

                for token in filter_tokens:
                    token_split = token.split("=")
                    key = token_split[0]
                    value = token_split[1]

                    if key == "src" or key == "dst":
                        if "::" in value:
                            filter_string_ipv6 += f"match ip6 {key} {value} "
                        else:
                            filter_string += f"match ip {key} {value} "
                    else:
                        filter_string += f"match ip {key} {value} "
                        filter_string_ipv6 += f"match ip6 {key} {value} "
                    if key == "sport" or key == "dport":
                        filter_string += "0xffff "
                        filter_string_ipv6 += "0xffff "

            except IndexError:
                logging.error("Error: Invalid filter parameters")

            if filter_string:
                filter_strings.append(filter_string)
            if filter_string_ipv6:
                filter_strings_ipv6.append(filter_string_ipv6)

        return filter_strings, filter_strings_ipv6


@dataclass
class TcFilter(Filter):
    _include_list: list = None
    _nic: str = None
    _ip_version: str = None
    _type: str = None

    def __post_init__(self):
        self._ip_version_check(self._ip_version)
        self._type_check(self._type)

        if self._type == "exclude":
            logging.debug(f"Excluding the following from network impairment for {self._ip_version}:")
            self._priority = (2, 1)[self._ip_version == "ip"]
        else:
            logging.debug(f"Including the following for network impairment for {self._ip_version}:")
            self._priority = (4, 3)[self._ip_version == "ip"]

        self._flowid = ("1:3", "1:2")[self._type == "exclude"]
        self._apply_filter()

    def _apply_filter(self):
        for rule in self._include_list:
            filter_cmd = f"tc filter add dev {self._nic} protocol {self._ip_version} " \
                         f"parent 1:0 prio {self._priority} u32 {rule}flowid {self._flowid}"
            logging.debug(filter_cmd)
            check_call(filter_cmd)

    def _ip_version_check(self, ip_version):
        _allowed_ip_versions = ["ip", "ipv6"]
        if not (ip_version in _allowed_ip_versions):
            raise Exception("Invalid ip_version parameter")
        else:
            return

    def _type_check(self, type):
        _allowed_types = ["include", "exclude"]
        if not (type in _allowed_types):
            raise Exception("Invalid type parameter")
        else:
            return
