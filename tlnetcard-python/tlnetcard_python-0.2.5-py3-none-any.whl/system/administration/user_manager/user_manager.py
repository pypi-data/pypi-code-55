# user_manager.py
# Ethan Guthrie
# 04/06/2020
""" Allows user and permission settings to be configured. """

# Standard library.
from os import remove
from time import sleep
from typing import Any, Dict
# Related third-party library.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# Required internal classes/functions.
from tlnetcard_python.login import Login
from tlnetcard_python.system.administration.batch_configuration import BatchConfiguration

class UserManager:
    """ Class for the UserManager object. """
    def __init__(self, login_object: Login) -> None:
        """ Initializes the UserManager object. """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/adm_user.asp"
        self._post_url = login_object.get_base_url() + "/delta/adm_user"
        self._batch_object = BatchConfiguration(self._login_object)
    def disable_radius(self) -> None:
        """ Disables RADIUS authentication. """
        # Generating payload.
        user_data = {
            "radius": "0"
        }

        # Uploading console configuration.
        self._login_object.get_session().post(self._post_url, data=user_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def enable_radius(self) -> None:
        """ Enables RADIUS authentication. """
        # Generating payload.
        user_data = {
            "radius": "1"
        }

        # Uploading console configuration.
        self._login_object.get_session().post(self._post_url, data=user_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def get_permissions(self, user: str = "Administrator") -> Dict[str, bool]:
        """ GETs the permissions for the provided user. """
        # Creating permission type list.
        permission_types = ["Login User", "Framed User", "Callback Login", "Callback Framed",
                            "Outbound", "Administrative", "NAS Prompt", "Authenticate Only",
                            "Callback NAS Prompt", "Call Check", "Callback Administrative"]
        # Initializing dictionary.
        user_permissions = {}
        # Setting user type string.
        if user == "Administrator":
            user_type = "RADIUS Admin User"
        elif user == "Device Manager":
            user_type = "RADIUS Device User"
        elif user == "Read Only User":
            user_type = "RADIUS User User"
        else:
            return -1

        # GETing system configuration and writing lines to list.
        self._batch_object.download_system_configuration("system_config_temp.ini")
        with open("system_config_temp.ini", "r") as sys_config_file:
            sys_config = sys_config_file.readlines()

        # Parsing list for permissions code.
        for line in sys_config:
            if line.find(user_type) != -1:
                permission_code = int(line.rstrip('\n').split("=")[1])
                break

        # Converting permissions code to binary string.
        permission_code_bin = format(permission_code, '011b')
        # Reversing binary.
        permission_code_bin = permission_code_bin[::-1]

        # Parsing binary to create dictionary.
        for i in range(0, len(permission_types)):
            user_permissions[permission_types[i]] = bool(int(permission_code_bin[i]))

        # Cleaning up.
        remove("system_config_temp.ini")

        return user_permissions
    def get_server_info(self) -> Dict[str, Any]:
        """ GETs information about the RADIUS server. """
        # GETing User Manager page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for server IP.
        addr = resp.text.find("NAME=\"USR_RADSRV\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)
        server_ip = resp.text[start_index:end_index]

        # Parsing response for server secret.
        addr = resp.text.find("NAME=\"USR_RADSEC\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)
        server_secret = resp.text[start_index:end_index]

        # Parsing response for server port.
        addr = resp.text.find("NAME=\"USR_RADPRT\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)
        server_port = int(resp.text[start_index:end_index])

        # Generating dictionary.
        server_data = {
            "IP": server_ip,
            "Secret": server_secret,
            "Port": server_port
        }

        return server_data
    def get_user(self, user: str = "Administrator") -> Dict[str, Any]:
        """ GETs information about the provided user. """
        # Setting user num string.
        if user == "Administrator":
            num = "1"
        elif user == "Device Manager":
            num = "2"
        elif user == "Read Only User":
            num = "3"
        else:
            return -1

        # GETing User Manager page.
        resp = self._login_object.get_session().get(self._get_url)

        # Parsing response for user name.
        addr = resp.text.find("NAME=\"account" + num + "\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)
        name = resp.text[start_index:end_index]

        # Parsing response for user password.
        addr = resp.text.find("NAME=\"passwd" + num + "\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)
        password = resp.text[start_index:end_index]

        # Parsing response for user WAN access.
        addr = resp.text.find("NAME=\"limit" + num + "\"")
        start_index = str(resp.text).find("VALUE=", addr) + 7
        end_index = str(resp.text).find("\"", start_index)
        wan_access = bool(int(resp.text[start_index:end_index]))

        # Generating dictionary.
        user_data = {
            "Type": user,
            "Name": name,
            "Password": password,
            "WAN Access": wan_access
        }

        return user_data
    def set_permissions(self, user: str = "Administrator", login_user: bool = False,
                        framed_user: bool = False, callback_login: bool = False,
                        callback_framed: bool = False, outbound: bool = False,
                        administrative: bool = False, nas_prompt: bool = False,
                        authenticate_only: bool = False, callback_nas_prompt: bool = False,
                        call_check: bool = False, callback_administrative: bool = False,
                        selenium: bool = False) -> int:
        """ Sets permissions for the provided user. """
        # Generating required dictionaries.
        user_types = {
            "Administrator": ['RADIUS Admin User', 0],
            "Device Manager": ['RADIUS Device User', 20],
            "Read Only User": ['RADIUS User User', 40]
        }
        permissions = {
            0: login_user,
            1: framed_user,
            2: callback_login,
            3: callback_framed,
            4: outbound,
            5: administrative,
            6: nas_prompt,
            7: authenticate_only,
            8: callback_nas_prompt,
            9: call_check,
            10: callback_administrative
        }

        # Exiting if invalid user type was specified.
        if user not in user_types:
            return -1

        if not selenium:
            # Generating binary permissions string.
            permission_code_bin = ""
            for i in permissions:
                permission_code_bin += str(int(permissions[i]))

            # Reversing string.
            permission_code_bin = permission_code_bin[::-1]
            # Converting binary string to integer.
            permission_code = int(permission_code_bin, 2)

            # GETing system configuration and writing lines to list.
            self._batch_object.download_system_configuration("system_config_temp.ini")
            with open("system_config_temp.ini", "r") as sys_config_file:
                sys_config = sys_config_file.readlines()

            # Parsing list and adding permissions code.
            updated_sys_config = []
            for line in sys_config:
                if line.find(user_types[user][0]) != -1:
                    updated_sys_config.append(user_types[user][0] + " Type="
                                              + str(permission_code) + "\n")
                else:
                    updated_sys_config.append(line)

            # Writing updated config to file.
            with open("system_config_temp.ini", "w") as sys_config_file:
                sys_config_file.writelines(updated_sys_config)

            # Uploading updated batch configuration file.
            self._batch_object.upload_system_configuration("system_config_temp.ini")

            # Cleaning up.
            remove("system_config_temp.ini")
        else:
            # Configuring Selenium to run headless (i.e. without a GUI).
            browser_options = Options()
            browser_options.add_argument("--headless")
            browser = webdriver.Chrome(options=browser_options)
            # Getting webpage.
            browser.get(self._get_url)
            # Adding cookies from requests session.
            requests_cookies = self._login_object.get_session().cookies.get_dict()
            for cookie in requests_cookies:
                browser.add_cookie({'name': cookie,
                                    'domain': self._login_object.get_host(),
                                    'value': requests_cookies[cookie]})
            # Getting webpage now that cookies are installed.
            browser.get(self._get_url)
            # A very brief sleeping period to let elements load.
            sleep(0.5)

            # Clicking boxes.
            for i in permissions:
                if (permissions[i] and
                        not browser.find_element_by_id(str(i + user_types[user][1])).is_selected()):
                    browser.find_element_by_id(str(i + user_types[user][1])).click()
                elif (not permissions[i] and
                      browser.find_element_by_id(str(i + user_types[user][1])).is_selected()):
                    browser.find_element_by_id(str(i + user_types[user][1])).click()

            # Clicking submit and closing browser.
            browser.find_element_by_id("@adm_console#11").click()
            browser.close()

        return 0
    def set_server_info(self, server: str, secret: str, port: int = 1812) -> None:
        """ Sets information for the RADIUS server. """
        # Generating payload.
        user_data = {
            "radius": "1",
            "USR_RADSRV": server,
            "USR_RADSEC": secret,
            "USR_RADPRT": str(port)
        }

        # Uploading console configuration.
        self._login_object.get_session().post(self._post_url, data=user_data,
                                              verify=self._login_object.get_reject_invalid_certs())
    def set_user(self, username: str, passwd: str, wan_access: int = False,
                 user: str = "Administrator") -> None:
        """ Sets information for the provided user. """
        # Setting user num string.
        if user == "Administrator":
            num = "1"
        elif user == "Device Manager":
            num = "2"
        elif user == "Read Only User":
            num = "3"
        else:
            return -1

        # Generating payload.
        user_data = {
            "account" + num: username,
            "passwd" + num: passwd,
            "limit" + num: str(int(wan_access))
        }

        # Uploading console configuration.
        self._login_object.get_session().post(self._post_url, data=user_data,
                                              verify=self._login_object.get_reject_invalid_certs())
        return 0
