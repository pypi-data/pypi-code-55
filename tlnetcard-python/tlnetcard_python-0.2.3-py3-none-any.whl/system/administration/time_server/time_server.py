# time_server.py
# Ethan Guthrie
# 04/17/2020
""" Allows TimeServer to be updated or removed (i.e. switch to manual time). """

class TimeServer:
    """ Class for the TimeServer object. """
    def __init__(self, login_object):
        """ Initializes the TimeServer object. """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/adm_time.asp"
        self._post_url = login_object.get_base_url() + "/delta/adm_time"
    def disable_daylight_savings(self):
        """ Disables daylight savings for SNTP. """
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "0",
            "NTP_DLS_EN": "0"
        }

        # Uploading time server configuration.
        self._login_object.get_session().post(self._post_url, data=time_server_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def enable_daylight_savings(self, start_date="04/01", end_date="11/01"):
        """ Enables daylight savings from the start date to the end date for SNTP. """
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "0",
            "NTP_DLS_EN": "1",
            "NTP_DLS_SDATE": start_date,
            "NTP_DLS_EDATE": end_date
        }

        # Uploading time server configuration.
        self._login_object.get_session().post(self._post_url, data=time_server_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def enable_sntp(self):
        """ Enables SNTP. """
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "0"
        }

        # Uploading time server configuration.
        self._login_object.get_session().post(self._post_url, data=time_server_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def get_primary_server(self):
        """ GETs the primary time server for SNTP and returns it. """
        # GETing time server page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for primary server.
        addr = resp.html.find("NTP_IP1")
        start_index = str(addr).find("value=") + 7
        end_index = str(addr).find("'", start_index)

        return addr[start_index:end_index]
    def get_secondary_server(self):
        """ GETs the secondary time server for SNTP and returns it. """
        # GETing time server page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for primary server.
        addr = resp.html.find("NTP_IP2")
        start_index = str(addr).find("value=") + 7
        end_index = str(addr).find("'", start_index)

        return addr[start_index:end_index]
    def set_manual_time(self, date="01/01/2000", time="00:00:00"):
        """ Sets the time manually. """
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "1",
            "NTP_USE_PCTIME": "0",
            "NTP_SYSDATE": date,
            "NTP_SYSTIME": time
        }

        # Uploading time server configuration.
        self._login_object.get_session().post(self._post_url, data=time_server_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def set_primary_server(self, server):
        """ Sets the primary time server for SNTP. """
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "0",
            "NTP_IP1": server
        }

        # Uploading time server configuration.
        self._login_object.get_session().post(self._post_url, data=time_server_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def set_secondary_server(self, server):
        """ Sets the secondary time server for SNTP. """
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "0",
            "NTP_IP2": server
        }

        # Uploading time server configuration.
        self._login_object.get_session().post(self._post_url, data=time_server_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def set_time_zone(self, offset="GMT"):
        """ Sets the time zone for SNTP. """
        # Converting string to list value.
        offsets = ["GMT-12", "GMT-11", "GMT-10", "GMT-09", "GMT-08", "GMT-07",
                   "GMT-06", "GMT-05", "GMT-04", "GMT-03:30", "GMT-03", "GMT-02",
                   "GMT-01", "GMT", "GMT+01", "GMT+02", "GMT+03", "GMT+03:30",
                   "GMT+04", "GMT+05", "GMT+05:30", "GMT+06", "GMT+07", "GMT+08",
                   "GMT+09", "GMT+10", "GMT+11", "GMT+12"]
        zone = -1
        for i in range(0, len(offsets)):
            if offset == offsets[i]:
                zone = i
                break

        # Checking if zone value was set (otherwise an improper offset value was provided).
        if zone == -1:
            print("Invalid time zone specified!")
            return -1

        # Generating payload.
        time_server_data = {
            "NTP_MANU": "0",
            "NTP_ZONE": str(zone)
        }

        # Uploading time server configuration.
        self._login_object.get_session().post(self._post_url, data=time_server_data,
                                              verify=self._login_object.get_reject_invalid_certs())
        return 0
    def use_local_time(self):
        """ Sets the manual time to this PC's time. """
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "1",
            "NTP_USE_PCTIME": "1"
        }

        # Uploading time server configuration.
        self._login_object.get_session().post(self._post_url, data=time_server_data,
                                              verify=self._login_object.get_reject_invalid_certs())
