# in_out_parameters.py
# Ethan Guthrie
# 05/26/2020
""" Allows UPS input and output power levels to be read. """

# Standard library.
from typing import Any, Dict
# Required internal classes/functions.
from tlnetcard_python.login import Login
from tlnetcard_python.monitor.information.information import get_with_snmp, scrape_with_selenium

class InOutParameters:
    """ Class for the InOutParameters object. """
    def __init__(self, login_object: Login) -> None:
        """ Initializes the InOutParameters object. """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/ups/info_io.asp"
    def get_bypass_measurements(self, snmp: bool = True, snmp_user: str = None,
                                snmp_auth_key: str = None, snmp_priv_key: str = None,
                                timeout: int = 10) -> Dict[str, Any]:
        """ Gets battery bypass measurements. """
        if snmp:
            # SNMP will be used to get values. This is the preferred method.
            # Generating SNMP ID dictionary.
            snmp_dict = {
                'Frequency': 'iso.3.6.1.2.1.33.1.5.1', # In decihertz
                                                       # (i.e. divide this value by 10).
                'Voltage': 'iso.3.6.1.2.1.33.1.5.3.1.2.1',
                'Current': 'iso.3.6.1.2.1.33.1.5.3.1.3.1', # In deciamps
                                                           # (i.e. divide this value by 10).
                'Power': 'iso.3.6.1.2.1.33.1.5.3.1.4.1'
            }

            # Getting values.
            freq, volts, curr, power = get_with_snmp(self._login_object.get_host(),
                                                     [snmp_dict[i] for i in snmp_dict], snmp_user,
                                                     snmp_auth_key, snmp_priv_key, timeout)

            # Generating out dictionary.
            out = {
                'Frequency (Hz)': float(freq)/10,
                'Voltage (V)': float(volts),
                'Current (A)': float(curr)/10,
                'Power (Watt)': int(power)
            }
        else:
            # Selenium will be used to scrape values. This method is slower than using SNMP.
            # Getting values.
            freq, volts, curr, power = scrape_with_selenium(self._login_object.get_host(),
                                                            ["UPS_BYFREQ1", "UPS_BYVOLT1",
                                                             "UPS_BYAMP1", "UPS_BYPOWER1"],
                                                            self._get_url,
                                                            self._login_object.get_session(),
                                                            timeout)

            # Generating out dictionary.
            out = {
                'Frequency (Hz)': float(freq),
                'Voltage (V)': float(volts),
                'Current (A)': float(curr),
                'Power (Watt)': int(power)
            }
        return out
    def get_input_measurements(self, snmp: bool = True, snmp_user: str = None,
                               snmp_auth_key: str = None, snmp_priv_key: str = None,
                               timeout: int = 10) -> Dict[str, Any]:
        """ Gets battery input measurements. """
        if snmp:
            # SNMP will be used to get values. This is the preferred method.
            # Generating SNMP ID dictionary.
            snmp_dict = {
                'Frequency': 'iso.3.6.1.2.1.33.1.3.3.1.2.1', # In decihertz
                                                             # (i.e. divide this number by 10).
                'Voltage': 'iso.3.6.1.2.1.33.1.3.3.1.3.1',
            }

            # Getting values.
            freq, volts = get_with_snmp(self._login_object.get_host(),
                                        [snmp_dict[i] for i in snmp_dict], snmp_user, snmp_auth_key,
                                        snmp_priv_key, timeout)

            # Generating out dictionary.
            out = {
                'Frequency (Hz)': float(freq)/10,
                'Voltage (V)': float(volts)
            }
        else:
            # Selenium will be used to scrape values. This method is slower than using SNMP.
            # Getting values.
            freq, volts = scrape_with_selenium(self._login_object.get_host(),
                                               ["UPS_INFREQ1", "UPS_INVOLT1"], self._get_url,
                                               self._login_object.get_session(), timeout)

            # Generating out dictionary.
            out = {
                'Frequency (Hz)': float(freq),
                'Voltage (V)': float(volts),
            }
        return out
    def get_output_measurements(self, snmp: bool = True, snmp_user: str = None,
                                snmp_auth_key: str = None, snmp_priv_key: str = None,
                                timeout: int = 10) -> Dict[str, Any]:
        """ Gets battery output measurements. """
        if snmp:
            # SNMP will be used to get values. This is the preferred method.
            # Generating SNMP ID dictionary.
            snmp_dict = {
                'Output': 'iso.3.6.1.2.1.33.1.4.1',
                'Frequency': 'iso.3.6.1.2.1.33.1.4.2', # In decihertz
                                                       # (i.e. divide this value by 10).
                'Voltage': 'iso.3.6.1.2.1.33.1.4.4.1.2.1',
                'Current': 'iso.3.6.1.2.1.33.1.4.4.1.3.1', # In deciamps
                                                           # (i.e. divide this value by 10).
                'Power': 'iso.3.6.1.2.1.33.1.4.4.1.4.1',
                'Loading': 'iso.3.6.1.2.1.33.1.4.4.1.5.1'
            }

            # Getting values.
            out, freq, volts, curr, power, load = get_with_snmp(self._login_object.get_host(),
                                                                [snmp_dict[i] for i in snmp_dict],
                                                                snmp_user, snmp_auth_key,
                                                                snmp_priv_key, timeout)
            # Output source status is actually returned as an integer whose values map as follows:
            status_dict = {
                1: 'Other',
                2: 'None',
                3: 'Normal',
                4: 'Bypass',
                5: 'Battery',
                6: 'Booster',
                7: 'Reducer'
            }

            # Generating out dictionary.
            out = {
                'Output Source': status_dict[int(out)],
                'Frequency (Hz)': float(freq)/10,
                'Voltage (V)': float(volts),
                'Current (A)': float(curr)/10,
                'Power (Watt)': int(power),
                'Loading (%)': int(load)
            }
        else:
            # Selenium will be used to scrape values. This method is slower than using SNMP.
            # Getting values.
            host = self._login_object.get_host()
            session = self._login_object.get_session()
            out, freq, volts, curr, power, load = scrape_with_selenium(host,
                                                                       ["UPS_OUTSRC", "UPS_OUTFREQ",
                                                                        "UPS_OUTVOLT1",
                                                                        "UPS_OUTAMP1",
                                                                        "UPS_OUTPOWER1",
                                                                        "UPS_OUTLOAD1"],
                                                                       self._get_url, session,
                                                                       timeout)

            # Generating out dictionary.
            out = {
                'Output Source': out,
                'Frequency (Hz)': float(freq),
                'Voltage (V)': float(volts),
                'Current (A)': float(curr),
                'Power (Watt)': int(power),
                'Loading (%)': int(load)
            }
        return out
