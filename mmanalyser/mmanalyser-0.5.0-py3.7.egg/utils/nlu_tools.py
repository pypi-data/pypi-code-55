import json
import logging
import requests


class NluTools(object):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def httpcall(self, url, req):
        try:
            response = requests.post(
                    url, json.dumps(req).encode("utf8"), timeout=10)
        except Exception as e:
            self.logger.exception("nlu error[%s]", e)
            return None
        if response.status_code != 200:
            return None
        return json.loads(response.text)

    def get_rationality(self, array, rationality_service_url):
        req = {
            "header": {'Content-Type': 'application/json'},
            "traffic_paramsDict": {
                "text": array,
                "prob": False,
                "strategy": "seq"
            }
        }

        result = self.httpcall(rationality_service_url, req)
        if result is None:
            return []

        if result['status']:
            return result['result']['ppl']
        else:
            self.logger.error("Get Rationality Failed - Error Msg: %s", result['info'])
            return []

