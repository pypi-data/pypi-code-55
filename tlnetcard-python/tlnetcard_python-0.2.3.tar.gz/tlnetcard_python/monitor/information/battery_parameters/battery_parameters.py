# battery_parameters.py
# Ethan Guthrie
# 05/14/2020
""" Allows battery parameters to be read. """
# Required internal functions.
from tlnetcard_python.monitor.information.information import get_with_snmp, scrape_with_selenium

class BatteryParameters:
    """ Class for the Battery_Parameters object. """
    def __init__(self, login_object):
        """ Initializes the Battery_Parameters object. """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/ups/info_battery.asp"
    def get_battery_status(self, snmp=True, snmp_user=None,
                           snmp_auth_key=None, snmp_priv_key=None, timeout=10):
        """ Gets battery status information. """
        if snmp:
            # SNMP will be used to get the value. This is the preferred method.
            # Generating SNMP ID dictionary.
            snmp_dict = {
                'Battery Status': 'iso.3.6.1.2.1.33.1.2.1',
                'On Battery Time': 'iso.3.6.1.2.1.33.1.2.2'
            }

            # Getting values.
            batt_stat, batt_time = get_with_snmp([snmp_dict[i] for i in snmp_dict],
                                                 self._login_object.get_host(), snmp_user,
                                                 snmp_auth_key, snmp_priv_key, timeout)
            # Battery status is actually returned as an integer whose values map as follows:
            status_dict = {
                1: 'Unknown',
                2: 'Normal',
                3: 'Low',
                4: 'Depleted'
            }

            # Generating out dictionary.
            out = {
                'Battery Status': status_dict[int(batt_stat)],
                'On Battery Time (s)': int(batt_time)
            }
        else:
            # Selenium will be used to scrape the value. This method is slower than using SNMP.
            # Getting values.
            batt_stat, batt_time = scrape_with_selenium(self._login_object.get_host(),
                                                        self._login_object.get_session(),
                                                        self._get_url,
                                                        ["UPS_BATTSTS", "UPS_ONBATTTIME"],
                                                        timeout)

            # Generating out dictionary.
            out = {
                'Battery Status': batt_stat,
                'On Battery Time (s)': int(batt_time)
            }
        return out
    def get_battery_measurements(self, snmp=True, snmp_user=None,
                                 snmp_auth_key=None, snmp_priv_key=None, timeout=10):
        """ Gets information about battery capacity, temperature, and voltage. """
        if snmp:
            # SNMP will be used to get the value. This is the preferred method.
            # Generating SNMP ID dictionary.
            snmp_dict = {
                'Battery Capacity': 'iso.3.6.1.2.1.33.1.2.4',
                'Voltage': 'iso.3.6.1.2.1.33.1.2.5', # In decivolts (i.e. divide this value by 10).
                'Temperature': 'iso.3.6.1.2.1.33.1.2.7',
                'Remaining Minutes': 'iso.3.6.1.2.1.33.1.2.3',
            }

            # Getting values.
            batt_cap, volts, temp, rem_mins = get_with_snmp([snmp_dict[i] for i in snmp_dict],
                                                            self._login_object.get_host(),
                                                            snmp_user, snmp_auth_key,
                                                            snmp_priv_key, timeout)

            # Generating out dictionary.
            mins = int(rem_mins)
            hours = int((mins - (mins % 60))/60)
            rem_time = '{hours:02d}:{mins:02d}'.format(hours=hours, mins=mins % 60)
            out = {
                'Battery Capacity (%)': int(batt_cap),
                'Voltage (V)': float(int(volts)/10),
                'Temperature (°C)': int(temp),
                'Remaining Time (HH:MM)': rem_time
            }
        else:
            # Selenium will be used to scrape the value. This method is slower than using SNMP.
            # Getting values.
            batt_cap, volts, temp, time, = scrape_with_selenium(self._login_object.get_host(),
                                                                self._login_object.get_session(),
                                                                self._get_url,
                                                                ["UPS_BATTLEVEL",
                                                                 "UPS_BATTVOLT",
                                                                 "UPS_TEMP",
                                                                 "UPS_BATTREMAIN"],
                                                                timeout)

            # Generating out dictionary.
            out = {
                'Battery Capacity (%)': int(batt_cap),
                'Voltage (V)': float(volts),
                'Temperature (°C)': int(temp),
                'Remaining Time (HH:MM)': time
            }
        return out
    def get_last_replacement_date(self, timeout=10):
        """ Gets the last date the UPS battery was changed. """
        # This value is not available with SNMP.
        return scrape_with_selenium(self._login_object.get_host(), self._login_object.get_session(),
                                    self._get_url, ["UPS_BATTLAST"], timeout)[0]
    def get_next_replacement_date(self, timeout=10):
        """ Gets the next date the UPS battery should be changed. """
        # This value is not available with SNMP.
        return scrape_with_selenium(self._login_object.get_host(), self._login_object.get_session(),
                                    self._get_url, ["UPS_BATTNEXT"], timeout)[0]
