import requests
import random
import time


class SendData:
    def __init__(self, hostname, ga_config):

        self._hostname = hostname
        self._ga_config = ga_config

    def _ga_cid(self):
        prefix = random.randint(1, 0x7FFFFFFF)
        epoch = time.time()
        return f"{prefix}.{epoch}"

    def _ga_send_data(self, data):
        # Send Data to Google Analytics
        # https://developers.google.com/analytics/devguides/collection/protocol/v1/devguide#event

        payload = {
            "payload_data": "",
        }
        payload.update(data)

        result = requests.get(
            "https://ssl.google-analytics.com/collect", params=payload
        )

        result.raise_for_status()
        return result

    def ga_send_pageview(self, page, title, product_id, user_id=None):
        # Send Pageview Function for Server-Side Google Analytics
        data = dict(
            v=1,
            tid=self._ga_config,
            cid=self._ga_cid(),
            t="pageview",
            dh=self._hostname,  # Document Hostname "gearside.com"
            dp=page,  # Page "/something"
            dt=title,  # Title
            cd1=product_id,  # Custom dimension
        )
        if user_id:
            data["cd2"] = user_id

        return self._ga_send_data(data)
