from dataclasses import dataclass
import pendulum
import hashlib
import base64


@dataclass(order=False)
class APICredentials:
    """
    transfermovil credentials class

    @:param username: ecommerce username
    @:param source: ecommerce id
    @:param seed: ecommerce seed

    """
    username: str
    source: str
    seed: str

    def __encodepass__(self,text : str = None) -> str:

        if not isinstance(text,str) or len(text) == 0:
            raise Exception("Encode text cannot be empty")

        hash_string = hashlib.sha512(text.encode()).digest()
        encode64 = base64.b64encode(hash_string)
        encode64_string = str(encode64)
        return encode64_string[2:-1]


    def getheaders(self) -> dict:

        if not isinstance(self.username,str) or len(self.username) == 0:
            raise Exception("Incorrect Username")

        elif not isinstance(self.source,str) or len(self.source) == 0:
            raise Exception("Incorrect Source")

        elif not isinstance(self.seed,str) or len(self.seed) == 0:
            raise Exception("Incorrect Seed")

        current_date = pendulum.now()
        headers = {"Content-Type": "application/json",
                   "username": self.username,
                   "source": self.source,
                   "password": self.__encodepass__(
                       f"{self.username}{current_date.day}{current_date.month}{current_date.year}{self.seed}{self.source}")}
        return headers
    

