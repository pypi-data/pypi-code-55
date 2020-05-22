from dataclasses import dataclass
from requests.auth import HTTPBasicAuth

@dataclass(order=False)
class APICredentials:
    """
    ecrm Credentials class

    @:param username: ecrm app username
    @:param password: ecrm app password

    """
    username: str
    password: str

    def getAuth(self) -> HTTPBasicAuth:
        if not isinstance(self.username, str) or len(self.username) == 0:
            raise Exception("Incorrect Username")

        elif not isinstance(self.password, str) or len(self.password) == 0:
            raise Exception("Incorrect password")

        return HTTPBasicAuth(username=self.username, password=self.password)



