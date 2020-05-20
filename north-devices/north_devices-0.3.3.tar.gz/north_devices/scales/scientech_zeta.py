from typing import List, Tuple, Union, Optional
import logging
import time
import math
from ftdi_serial import Serial, SerialReadTimeoutException

logger = logging.getLogger(__name__)


class ScientechZeta:
    GRAMS = 'GRAMS'
    KG = 'KG'
    MG = 'MG'

    @staticmethod
    def parse_weight_response(response: bytes) -> float:
        stripped = response.strip(b'\r\n ')
        split = stripped.split(b' ')

        try:
            return float(split[0])
        except ValueError:
            return float('nan')

    def __init__(self, serial: Serial, timeout: float=1, retry_timeout: float=0.1, units: str=GRAMS):
        self.logger = logger.getChild(self.__class__.__name__)
        self.serial = serial
        self.timeout = timeout
        self.retry_timeout = retry_timeout
        self.set_units(units)

    def request(self, request: bytes, retries: int=10, retry_timeout: float=0.1) -> bytes:
        try:
            self.logger.debug(f'Request: {request}')
            response_raw = self.serial.request(request + b'\r', line_ending=b'\r\n', timeout=self.timeout)
            response = response_raw.rstrip(b'\r\n')
            self.logger.debug(f'Response: {response}')

            if response.startswith(b'?'):
                if retries <= 0:
                    raise ScientechZetaResponseError(f'Error response for request: {request}')

                self.logger.warning(f'Error response: {response}, retrying {retries} times')

                # time.sleep(retry_timeout)
                return self.request(request, retries=retries-1)

            return response

        except SerialReadTimeoutException:
            self.logger.warning(f'Request timeout, retrying {retries} times')
            if retries <= 0:
                raise ScientechZetaRequestTimeout(f'Request timeout: {request}')

            time.sleep(retry_timeout)
            return self.request(request, retries=retries-1)

    def set_units(self, units: str):
        if units not in (self.GRAMS, self.KG, self.MG):
            raise ScientechZetaInvalidUnitsError(f'Invalid units: {units}')

        self.request(units.encode())

    def clear(self):
        self.logger.info('Clear')
        self.request(b'CLEAR')

    def tare(self):
        self.logger.info('Tare')
        self.request(b'TARE')
        time.sleep(0.5)

    def weigh(self, retries: int=5, retry_timeout: float=0.1):
        response = self.request(b'SEND')

        if response.strip().startswith(b'OL'):
            return float('nan')

        weight = self.parse_weight_response(response)

        if len(response) < 10 or math.isnan(weight):
            if retries <= 0:
                raise ScientechZetaResponseError(f'Invalid weigh response: {response}')

            self.logger.warning(f'Invalid weigh response: {response}, retrying {retries} more times')
            time.sleep(retry_timeout)
            return self.weigh(retries - 1)

        time.sleep(0.1)
        return weight

    def settled_weigh(self, delta: float=0.005, matching: int=3, timeout: float=60.0, retry_timeout: float=0.5):
        weights = []
        start_time = time.time()

        while time.time() - start_time < timeout:
            weight = self.weigh()

            if len(weights) >= matching - 1:
                matching_weights = [not math.isnan(w) and abs(weight - w) < delta for w in weights]

                if False not in matching_weights:
                    return weight

            weights = [weight] + weights
            weights = weights[:matching - 1]
            time.sleep(retry_timeout)

        raise ScientechZetaWeighTimeout(f'Timeout while waiting for weight to settle')


class ScientechZetaError(Exception):
    pass


class ScientechZetaRequestTimeout(ScientechZetaError):
    pass


class ScientechZetaInvalidUnitsError(ScientechZetaError):
    pass


class ScientechZetaResponseError(ScientechZetaError):
    pass


class ScientechZetaWeighTimeout(ScientechZetaError):
    pass
