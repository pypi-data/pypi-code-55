import requests


class VaultConnector:

    def __init__(self, settings):
        self._settings = settings
        self._client_token = None

    def __enter__(self):
        self.authenticate()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def authenticate(self):
        res = requests.post(self._settings["auth_url"],
                            json={"jwt": self._settings["token"], "role": self._settings["app_name"]})
        res.raise_for_status()
        self._client_token = res.json()["auth"]["client_token"]

    def read_secrets(self):
        """ Fetch secrets from vault and return dict

        :return: dict: secrets
        """
        res = requests.get(self._settings["secrets_url"],
                           headers={"X-Vault-Token": self._client_token})
        res.raise_for_status()
        return res.json()["data"]

    def get_db_credentials(self, vault_path):
        """ Get new database credentials

        :param vault_path: str
        :return: string with username and password
        """
        res = requests.get(f"{self._settings['vault_address']}/v1/{vault_path}",
                           headers={"X-Vault-Token": self._client_token})

        res.raise_for_status()
        credentials = res.json()["data"]
        return f"{credentials['username']}:{credentials['password']}"
