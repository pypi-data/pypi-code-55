# login.py
# Ethan Guthrie
# 02/17/2020
""" Creates a logged-in session to the specified TLNETCARD using the provided credentials. """

# Standard library.
from getpass import getpass
from hashlib import md5
from warnings import filterwarnings
# Related third-party library.
from requests_html import HTMLSession
from urllib3.exceptions import InsecureRequestWarning

class Login:
    """ Class for the login object. A login object is required by all classes in this repository."""
    def __init__(self, user="admin", passwd="password", host="",
                 save_passwd=False, ssl=True, reject_invalid_certs=True):
        """ Initializes the login object. """
        # Saving values which will be used independently.
        self._host = host
        self._user = user
        self._reject_invalid_certs = reject_invalid_certs
        self._save_passwd = save_passwd
        self._ssl = ssl
        # Checking to see if password should be saved.
        if self._save_passwd:
            self._passwd = passwd
        else:
            self._passwd = ""
        # Generating base URL.
        if ssl and self._host != "":
            self._base_url = 'https://' + self._host
        else:
            self._base_url = 'http://' + self._host
        # Executing login if a host was specified.
        if self._host != "":
            self.perform_login(passwd)
    def get_base_url(self):
        """ Returns the base URL for TLNET Supervisor. """
        return self._base_url
    def get_host(self):
        """ Returns the host. """
        return self._host
    def get_reject_invalid_certs(self):
        """ Returns whether to accept invalid SSL certificates
        (i.e. self-signed SSL certificates). """
        return self._reject_invalid_certs
    def get_session(self):
        """ Returns the session. """
        return self._session
    def logout(self):
        """ Closes the session. """
        # Restoring warnings in case reject_invalid_certs flag is used.
        filterwarnings("default", category=InsecureRequestWarning)
        self._session.close()
    def perform_login(self, passwd):
        """ Logs into a new session. """
        # Ignoring self-signed SSL certificate warning when reject_invalid_certs is False.
        if not self._reject_invalid_certs:
            filterwarnings("ignore", category=InsecureRequestWarning)

        # Setting login URLs for future use.
        login_get_url = self._base_url + '/home.asp'
        login_post_url = self._base_url + '/delta/login'

        # Initializing session (to provide login persistence).
        session = HTMLSession()

        # Getting login screen HTML (so that Challenge can be retrieved).
        login_screen = session.get(login_get_url, verify=self._reject_invalid_certs, timeout=0.5)

        # Retrieving challenge from HTML.
        challenge_loc = login_screen.text.find('name="Challenge"')
        challenge = str(login_screen.text[challenge_loc + 24:challenge_loc + 32])

        # Generating 'Response' value (see login screen HTML for more details).
        response_str = self._user + passwd + challenge
        response = md5(response_str.encode('utf-8')).hexdigest()

        # Creating login payload.
        login_data = {
            'Username': self._user,
            'password': passwd,
            'Submitbtn': '      OK      ',
            'Challenge': challenge,
            'Response': response
        }

        # Logging in.
        session.post(login_post_url, data=login_data, verify=self._reject_invalid_certs)

        # Checking if login was successful.
        login_response = session.get(login_get_url,
                                     verify=self._reject_invalid_certs, timeout=0.5).text
        if login_response.find("login_title") != -1:
            print("login failed for host at URL " + self._host)
            session.close()
            return -1

        # Saving session.
        self._session = session
        return 0
    def set_host(self, host, passwd=""):
        """ Sets host and then calls perform_login(). """
        # Closing previous session (if there was one).
        if self._host != "":
            self.logout()
        # Saving host value.
        self._host = host
        # Setting base_url value.
        if self._ssl:
            self._base_url = 'https://' + self._host
        else:
            self._base_url = 'http://' + self._host
        # Checking if password was provided or if password was saved, and then logging in.
        if passwd != "":
            self.perform_login(passwd)
        elif self._save_passwd:
            self.perform_login(self._passwd)
        else:
            passwd = getpass()
            if self._save_passwd:
                self._passwd = passwd
            self.perform_login(getpass())
