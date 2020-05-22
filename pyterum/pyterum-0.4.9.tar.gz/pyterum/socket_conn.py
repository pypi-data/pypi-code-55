import time
import sys
from socket import socket, AF_UNIX, SHUT_RDWR

from pyterum import transmit
from pyterum.logger import logger

class SocketConn:
    def __init__(self, address:str, retry_policy:dict={str:int}):
        self.address:str = address
        self.socket:socket = None
        self.retry_policy = {
            "connect": -1 if "connect" not in retry_policy else retry_policy["connect"], # Initial connection
            "consume": 0 if "consume" not in retry_policy else retry_policy["consume"],
            "produce": 0 if "produce" not in retry_policy else retry_policy["produce"] 
        }
        self.retry_interval = 5

    # Retry infinitely if retries < 0
    # Raises an error if it cannot connect within the amount of retries
    def _connect(self, retries:int):
        while True:
            try:
                self.socket = socket(AF_UNIX)
                self.socket.connect(self.address)
                return
            except Exception as err:
                if retries == 0:
                    raise err
                retries_str = " " if retries < 0 else str(retries)+ " more time(s) "
                logger.warn(f"Couldn't reach host at {self.address}, retrying {retries_str}in {self.retry_interval} seconds...")
                time.sleep(self.retry_interval)

            if retries > 0:
                retries -= 1

    def connect(self):
        self._connect(self.retry_policy["connect"])

    def close(self):
        try:
            self.socket.shutdown(SHUT_RDWR)
            self.socket.close()
        except Exception as err:
            logger.warn(f"Could not close connection due to '{err}'")

    def _reconnect(self, retries:int):
        self.close()
        self._connect(retries)

    def _silent_reconnect(self, retries:int):
        try:
            self.close()
            self._connect(retries)
        except Exception:
            pass

    def reconnect(self):
        self.close()
        self.connect()

    def consumer(self):
        retries = self.retry_policy["consume"]
        retrying = False
        while True:
            try:
                # Decode messages send over this socket one-by-one
                msg = transmit.receive_from(self.socket)
                retrying = False
                yield msg
            except Exception as err:
                if not retrying:
                    logger.warn(f"Could not consume message due to '{err}'")

                if abs(retries) > 0:
                    retrying = True
                    retries -= 1 if retries > 0 else 0
                    logger.info(f"Retrying consume after attempting to reconnect")
                    self._silent_reconnect(0)
                    time.sleep(self.retry_interval)
                else:
                    logger.error(f"Failed to consume message")
                    raise err
        self.close()

    def produce(self, data):
        retries = self.retry_policy["produce"]
        retrying = False
        while True:
            try:
                transmit.send_to(self.socket, data)
                retrying = False
                break
            except Exception as err:
                if not retrying:
                    logger.warn(f"Could not produce message due to '{err}'")

                if abs(retries) > 0:
                    retrying = True
                    retries -= 1 if retries > 0 else 0
                    logger.info(f"Retrying produce of '{data}' after attempting to reconnect")
                    self._silent_reconnect(0)
                    time.sleep(self.retry_interval)
                else:
                    logger.error(f"Failed to produce message")
                    raise err