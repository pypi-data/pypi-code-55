import requests
from conf import conf
from time import sleep
from taskmanager.log import logger

headers = {
    "Authorization": "Bearer AKK63ZZCVJ4F32RMB6",
    "Content-type": "application/json-patch+json"
}

# create new request
def _createRequest(method, main, payload=None):
    retry = 0
    app = f'cmtworker-{main}-{conf.env}'
    logger.info(app)
    url = f'{conf.scale.url}/{app}/scale'
    logger.info(url)
    while retry < 3:
        if method == "patch":
            request = requests.patch(url, payload, headers = headers, verify = False)
        else:
            request = requests.get(url, headers=headers, verify=False)
        if request.status_code != 200:
            logger.error("Scale workers failed. request_status=%d", request.status_code)
            logger.error(request.json())
            retry += 1
            logger.info('retry for the %d time', retry)
            sleep(3)
        else:
            return request

# wait till number of containers equals target_number
def _wait(target_number, main):
    while True:
        current_spec = _getSpec(main)
        # number of containers is 0, leading to no "replicas" field in spec
        replicas = current_spec.get("replicas", 0)
        logger.info("n_containers=%d", replicas)
        if replicas == target_number:
            break
        sleep(10)
    logger.info("Scale workers succeed.")


# get spec of  current scale deployment
def _getSpec(main):
    r = _createRequest("get", main)
    current_spec = r.json().get("spec")
    return current_spec


# scale number of worker containers
def scale(main, target_number):
    if conf.scale.skip:
        return

    current_spec = _getSpec(main)
    # number of containers is 0, leading to no "replicas" field in spec
    operation = "replace"
    if current_spec is None or "replicas" not in current_spec:
        logger.info("current_spec: %s", current_spec)
        operation = "add"
    payload = '[{"op": "%s", "path": "/spec/replicas", "value": %d}]' % (operation, target_number)
    _createRequest("patch", main, payload)
    _wait(target_number, main)



