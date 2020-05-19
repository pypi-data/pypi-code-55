# information.py
# Ethan Guthrie
# 05/18/2020
""" Provides the get_with_snmp() and scrape_with_selenium() methods. """

# Standard library.
from time import sleep
# Related third-party library.
from pysnmp.hlapi import getCmd, SnmpEngine, UsmUserData, UdpTransportTarget
from pysnmp.hlapi import ContextData, ObjectType, ObjectIdentity
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Initialize class methods.
def get_with_snmp(snmp_ids, host, snmp_user=None, snmp_auth_key=None,
                  snmp_priv_key=None, timeout=10):
    """ Gets the provided SNMP values from their SNMP IDs. """
    out = []
    for i in snmp_ids:
        error_indication, error_status, error_index, var_binds = next(
            getCmd(SnmpEngine(),
                   UsmUserData(snmp_user, authKey=snmp_auth_key, privKey=snmp_priv_key),
                   UdpTransportTarget((host, 161),
                                      timeout=timeout, retries=1),
                   ContextData(),
                   ObjectType(ObjectIdentity(i)))
        )

        if error_indication:
            print(error_indication)
            return -1
        elif error_status:
            print('%s at %s' % (error_status.prettyPrint(),
                                error_index and var_binds[int(error_index) - 1][0] or '?'))
            return -1
        else:
            out.append(str(var_binds[0]).split("=")[-1])
    return out
def scrape_with_selenium(host, session, url, element_ids, timeout=10):
    """ Scrapes the provided web elements by their ID from the provided webpage. """
    # Configuring Selenium to run headless (i.e. without a GUI).
    browser_options = Options()
    browser_options.add_argument("--headless")
    browser = webdriver.Chrome(options=browser_options)
    # Getting card login page.
    browser.get(url)
    # Adding cookies from requests session to "login".
    requests_cookies = session.cookies.get_dict()
    for cookie in requests_cookies:
        browser.add_cookie({'name': cookie,
                            'domain': host,
                            'value': requests_cookies[cookie]})
    # Getting webpage again now that cookies are installed.
    browser.get(url)

    # Getting out dictionary.
    out = {}
    counter = 0.0
    while timeout > counter:
        for i in range(0, len(element_ids)):
            out[i] = browser.find_element_by_id(element_ids[i]).text
        if '' not in [out[j] for j in out]:
            break
        sleep(0.5)
        counter += 0.5

    return [out[i] for i in out]
