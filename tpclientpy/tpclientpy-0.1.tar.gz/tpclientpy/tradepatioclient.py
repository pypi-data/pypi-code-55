from time import time
import requests
import urllib.parse
import hashlib
import hmac
import math


class TradePatioClient:
    def __init__(self, api_key="", api_secret="", host=""):
        self.api_key = api_key
        self.api_secret = api_secret.encode("utf-8")
        self.host = host

    def get_exchanges(self):
        return self.request(
            body={},
            path="/api/v1/exchange",
            method="GET",
        ).json()

    def get_exchange_pairs(self, exchange):
        return self.request(
            body={},
            path="/api/v1/exchange/pair?exch=" + exchange,
            method="GET",
        ).json()

    def get_exchange_candles(self, exchange, pair, time_frame, period):
        return self.request(
            body={},
            path="/api/v1/exchange/pair/candles?ex=" + exchange + "&pair=" + pair + "&time-frame=" + time_frame + "&period=" + period,
            method="GET",
        ).json()

    def request(self, body, path, method):
        payload = {
            'nonce': math.floor(time()),
        }
        sig = self.make_sig(payload=payload)

        return requests.get(url=self.host + path, headers={'SHA512': sig})

    def make_sig(self, payload):
        payloadStr = urllib.parse.urlencode(payload).encode('utf8')
        sign = hmac.new(self.api_secret, payloadStr, hashlib.sha512).hexdigest()

        return self.api_key + "." + payloadStr.decode("utf-8") + "." + sign
