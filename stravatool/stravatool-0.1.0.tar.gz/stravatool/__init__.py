import configparser
import datetime
import os
import requests
from requests.compat import urljoin

class StravaTool:

    def access_token(self):
        """ Returns an api token. Will refresh if necessary """

        if datetime.datetime.now().timestamp() > self.config.getint(self.conf_section, 'expires_at'):
            # need a new access token

            # calls the api and gets updated information
            r = requests.post(urljoin(self.api_base, "oauth/token"), data={
                "client_id": self.config.get(self.conf_section, 'client_id'),
                "client_secret": self.config.get(self.conf_section, 'client_secret'),
                "grant_type": "refresh_token",
                "refresh_token": self.config.get(self.conf_section, 'refresh_token'),
            })
            r.raise_for_status()
            rdata = r.json()

            # sets the updated token information in the config file
            self.config.set(self.conf_section, 'access_token', rdata.get('access_token'))
            self.config.set(self.conf_section, 'refresh_token', rdata.get('refresh_token'))
            self.config.set(self.conf_section, 'expires_at', str(rdata.get('expires_at')))
            with open(self.config_file_path, "w") as configfile:
                self.config.write(configfile)

        return self.config.get(self.conf_section, 'access_token')

    def auth_headers(self):

        return {"Authorization": "Bearer {}".format(self.access_token())}

    def __init__(self, config_file, conf_section="strava"):

        self.config_file_path = os.path.abspath(config_file)
        self.conf_section = conf_section
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file_path)
        self.api_base = "https://www.strava.com/api/v3/"

