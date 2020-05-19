# Time_Server.py
# Ethan Guthrie
# 04/17/2020
# Allows Time_Server to be updated or removed (i.e. switch to manual time).

from requests_html import HTMLSession
from urllib3.exceptions import InsecureRequestWarning
from warnings import filterwarnings

class Time_Server:
    # Initializes the Time_Server object.
    def __init__(self, login_object):
        self._login_object = login_object
        self._get_url = login_object.getBaseURL() + "/en/adm_time.asp"
        self._post_url = login_object.getBaseURL() + "/delta/adm_time"
    # Disables daylight savings for SNTP.
    def disableDaylightSavings(self):
        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)
        
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "0",
            "NTP_DLS_EN": "0"
        }

        # Uploading time server configuration.
        self._login_object.getSession().post(self._post_url, data=time_server_data, verify=self._login_object.getRejectInvalidCerts())

        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return
    # Enables daylight savings from the start date to the end date for SNTP.
    def enableDaylightSavings(self, start_date="04/01", end_date="11/01"):
        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)
        
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "0",
            "NTP_DLS_EN": "1",
            "NTP_DLS_SDATE": start_date,
            "NTP_DLS_EDATE": end_date
        }

        # Uploading time server configuration.
        self._login_object.getSession().post(self._post_url, data=time_server_data, verify=self._login_object.getRejectInvalidCerts())

        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return
    # Enables SNTP.
    def enableSNTP(self):
        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)
        
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "0"
        }

        # Uploading time server configuration.
        self._login_object.getSession().post(self._post_url, data=time_server_data, verify=self._login_object.getRejectInvalidCerts())

        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return
    # GETs the primary time server for SNTP and returns it.
    def getPrimaryServer(self):
        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)
        
        # GETing time server page.
        r = self._login_object.getSession().get(self._get_url)

        # Parsing response for primary server.
        addr = r.html.find("NTP_IP1")
        start_index = str(addr).find("value=") + 7
        end_index = str(addr).find("'", start_index)

        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return addr[start_index:end_index]
    # GETs the secondary time server for SNTP and returns it.
    def getSecondaryServer(self):
        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)
        
        # GETing time server page.
        r = self._login_object.getSession().get(self._get_url)

        # Parsing response for primary server.
        addr = r.html.find("NTP_IP2")
        start_index = str(addr).find("value=") + 7
        end_index = str(addr).find("'", start_index)

        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return addr[start_index:end_index]
    # Sets the time manually.
    def setManualTime(self, date="01/01/2000", time="00:00:00"):
        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)
        
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "1",
            "NTP_USE_PCTIME": "0",
            "NTP_SYSDATE": date,
            "NTP_SYSTIME": time
        }

        # Uploading time server configuration.
        self._login_object.getSession().post(self._post_url, data=time_server_data, verify=self._login_object.getRejectInvalidCerts())

        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)
        
        return
    # Sets the primary time server for SNTP.
    def setPrimaryServer(self, server):
        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)
        
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "0",
            "NTP_IP1": server
        }

        # Uploading time server configuration.
        self._login_object.getSession().post(self._post_url, data=time_server_data, verify=self._login_object.getRejectInvalidCerts())

        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return
    # Sets the secondary time server for SNTP.
    def setSecondaryServer(self, server):
        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)
        
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "0",
            "NTP_IP2": server
        }

        # Uploading time server configuration.
        self._login_object.getSession().post(self._post_url, data=time_server_data, verify=self._login_object.getRejectInvalidCerts())

        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return
    # Sets the time zone for SNTP.
    def setTimeZone(self, offset="GMT"):
        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)
        
        # Converting string to list value.
        offsets = ["GMT-12", "GMT-11", "GMT-10", "GMT-09", "GMT-08", "GMT-07", "GMT-06", "GMT-05", "GMT-04", "GMT-03:30", "GMT-03", "GMT-02", "GMT-01", "GMT", "GMT+01", "GMT+02", "GMT+03", "GMT+03:30", "GMT+04", "GMT+05", "GMT+05:30", "GMT+06", "GMT+07", "GMT+08", "GMT+09", "GMT+10", "GMT+11", "GMT+12"]
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
        self._login_object.getSession().post(self._post_url, data=time_server_data, verify=self._login_object.getRejectInvalidCerts())

        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return
    # Sets the manual time to this PC's time.
    def useLocalTime(self):
        # Ignoring certificate warnings if Login object specifies.
        if not self._login_object.getRejectInvalidCerts():
            filterwarnings("ignore", category=InsecureRequestWarning)
        
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "1",
            "NTP_USE_PCTIME": "1"
        }

        # Uploading time server configuration.
        self._login_object.getSession().post(self._post_url, data=time_server_data, verify=self._login_object.getRejectInvalidCerts())

        # Restoring certificate warnings in case it was changed.
        filterwarnings("default", category=InsecureRequestWarning)

        return
