import requests
from time import sleep
from kctaskman.log import logger


class Scaler:

    def __init__(self, api_url, auth, deployment_name):
        self._deployment_name = deployment_name
        self._api_url = api_url
        self._headers = {
            "Authorization": auth,
            "Content-type": "application/json-patch+json"
        }

    def _req(self, method, payload=None):
        retry = 0
        url = f'{self._api_url}/deployments/{self._deployment_name}/scale'
        while retry < 3:
            if method == "patch":
                request = requests.patch(url, payload, headers=self._headers, verify=False)
            else:
                request = requests.get(url, headers=self._headers, verify=False)
            if request.status_code != 200:
                logger.error("Scale workers failed. request_status=%d", request.status_code)
                logger.error(request.json())
                retry += 1
                logger.info('retry for the %d time', retry)
                sleep(3)
            else:
                return request

    # wait till number of containers equals target_number
    def _wait(self, target_number):
        while True:
            current_spec = self._getSpec()
            # number of containers is 0, leading to no "replicas" field in spec
            replicas = current_spec.get("replicas", 0)
            logger.info("n_containers=%d", replicas)
            if replicas == target_number:
                break
            sleep(10)
        logger.info("Scale workers succeed.")

    # get spec of  current scale deployment
    def _getSpec(self):
        r = self._req("get")
        current_spec = r.json().get("spec")
        return current_spec

    # scale number of worker containers
    def scale(self, target_number):
        if not self._api_url:
            return

        current_spec = self._getSpec()
        # number of containers is 0, leading to no "replicas" field in spec
        operation = "replace"
        if current_spec is None or "replicas" not in current_spec:
            logger.info("current_spec: %s", current_spec)
            operation = "add"
        payload = '[{"op": "%s", "path": "/spec/replicas", "value": %d}]' % (operation, target_number)
        self._req("patch", payload)
        self._wait(target_number)
