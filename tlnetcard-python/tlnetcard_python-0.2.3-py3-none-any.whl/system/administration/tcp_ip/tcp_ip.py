# tcp_ip.py
# Ethan Guthrie
# 05/04/2020
""" Allows TCP/IP settings for IPv4/IPv6 to be configured. """

class TcpIp:
    """ Class for the TcpIp object. """
    def __init__(self, login_object):
        """ Initializes the TcpIp object. """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/adm_ipconfig.asp"
        self._post_url = login_object.get_base_url() + "/delta/adm_ipconfig"
    def disable_autonegotiation(self):
        """ Disables link speed autonegotiation. """
        # Generating payload.
        ip_data = {
            "SYS_AUTONEG": "0"
        }

        # Uploading TCP/IP configuration.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def disable_dhcp(self, protocol="IPv4"):
        """ Disables DHCP for the provided protocol. """
        # Checking protocol and generating payload.
        if protocol.find("4") != -1:
            ip_data = {
                "SYS_DHCP": "0"
            }
        elif protocol.find("6") != -1:
            ip_data = {
                "SYS_V6DHCP": "0"
            }
        else:
            return -1

        # Uploading TCP/IP configuration.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              verify=self._login_object.get_reject_invalid_certs())
        return 0
    def enable_autonetogiation(self):
        """ Enables link speed negotiation. """
        # Generating payload.
        ip_data = {
            "SYS_AUTONEG": "1"
        }

        # Uploading TCP/IP configuration.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def enable_dhcp(self, protocol="IPv4"):
        """ Enables DHCP for the provided protocol. """
        # Checking protocol and generating payload.
        if protocol.find("4") != -1:
            ip_data = {
                "SYS_DHCP": "1"
            }
        elif protocol.find("6") != -1:
            ip_data = {
                "SYS_V6DHCP": "1"
            }
        else:
            return -1

        # Uploading TCP/IP configuration.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              verify=self._login_object.get_reject_invalid_certs())
        return 0
    def get_dns_ip(self, protocol="IPv4"):
        """ GETs the DNS IP for the provided protocol. """
        # Checking protocol.
        if protocol.find("4") != -1:
            name = "SYS_DNS"
        elif protocol.find("6") != -1:
            name = "SYS_V6DNS"
        else:
            return -1

        # GETing TCP/IP page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for DNS address.
        addr = resp.text.find("NAME=\"" + name + "\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)
        return resp.text[start_index:end_index]
    def get_gateway_ip(self, protocol="IPv4"):
        """ GETs the Gateway IP for the provided protocol. """
        # Checking protocol.
        if protocol.find("4") != -1:
            name = "SYS_GATE"
        elif protocol.find("6") != -1:
            name = "SYS_V6GT"
        else:
            return -1

        # GETing TCP/IP page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for gateway IP address.
        addr = resp.text.find("NAME=\"" + name + "\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)
        return resp.text[start_index:end_index]
    def get_ip_addr(self, protocol="IPv4"):
        """ GETs the IP address for the provided protocol. """
        # Checking protocol.
        if protocol.find("4") != -1:
            name = "SYS_IP"
        elif protocol.find("6") != -1:
            name = "SYS_V6IP"
        else:
            return -1

        # GETing TCP/IP page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for IP address.
        addr = resp.text.find("NAME=\"" + name + "\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)
        return resp.text[start_index:end_index]
    def get_prefix_len(self):
        """ GETs the IPv6 prefix length. """
        # GETing TCP/IP page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for IPv6 prefix length.
        addr = resp.text.find("NAME=\"SYS_V6LEN\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)
        return resp.text[start_index:end_index]
    def get_search_domain(self):
        """ GETs the IPv4 search domain. """
        # GETing TCP/IP page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for IPv6 prefix length.
        addr = resp.text.find("NAME=\"SYS_DOMAIN\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)
        return resp.text[start_index:end_index]
    def get_subnet_mask(self):
        """ GETs the IPv4 subnet mask. """
        # GETing TCP/IP page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for IPv6 prefix length.
        addr = resp.text.find("NAME=\"SYS_MASK\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)
        return resp.text[start_index:end_index]
    def set_dns_ip(self, ip_addr, protocol="IPv4"):
        """ Sets the DNS IP for the provided protocol. """
        # Checking protocol and generating payload.
        if protocol.find("4") != -1:
            ip_data = {
                "SYS_DHCP": "0",
                "SYS_DNS": str(ip_addr)
            }
        elif protocol.find("6") != -1:
            ip_data = {
                "SYS_V6DHCP": "0",
                "SYS_V6DNS": str(ip_addr)
            }
        else:
            return -1

        # Uploading TCP/IP configuration.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              verify=self._login_object.get_reject_invalid_certs())
        return 0
    def set_gateway_ip(self, ip_addr, protocol="IPv4"):
        """ Sets the Gateway IP for the provided protocol. """
        # Checking protocol and generating payload.
        if protocol.find("4") != -1:
            ip_data = {
                "SYS_DHCP": "0",
                "SYS_GATE": str(ip_addr)
            }
        elif protocol.find("6") != -1:
            ip_data = {
                "SYS_V6DHCP": "0",
                "SYS_V6GW": str(ip_addr)
            }
        else:
            return -1

        # Uploading TCP/IP configuration.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              verify=self._login_object.get_reject_invalid_certs())
        return 0
    def set_ip_addr(self, ip_addr, protocol="IPv4"):
        """ Sets the IP address for the provided protocol. """
        # Checking protocol and generating payload.
        if protocol.find("4") != -1:
            ip_data = {
                "SYS_DHCP": "0",
                "SYS_IP": str(ip_addr)
            }
        elif protocol.find("6") != -1:
            ip_data = {
                "SYS_V6DHCP": "0",
                "SYS_V6IP": str(ip_addr)
            }
        else:
            return -1

        # Uploading TCP/IP configuration.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              verify=self._login_object.get_reject_invalid_certs())
        return 0
    def set_prefix_len(self, length):
        """ Sets the IPv6 prefix length. """
        # Generating payload.
        ip_data = {
            "SYS_V6DHCP": "0",
            "SYS_V6LEN": str(length)
        }

        # Uploading TCP/IP configuration.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def set_search_domain(self, domain):
        """ Sets the IPv4 search domain. """
        # Generating payload.
        ip_data = {
            "SYS_DHCP": "0",
            "SYS_DOMAIN": str(domain)
        }

        # Uploading TCP/IP configuration.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def set_subnet_mask(self, mask):
        """ Sets the IPv4 subnet mask. """
        # Generating payload.
        ip_data = {
            "SYS_DHCP": "0",
            "SYS_MASK": str(mask)
        }

        # Uploading TCP/IP configuration.
        self._login_object.get_session().post(self._post_url, data=ip_data,
                                              verify=self._login_object.get_reject_invalid_certs())
