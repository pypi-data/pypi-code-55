from kubernetes import client, config
from kubernetes.client.rest import ApiException
import base64
import time

config.load_kube_config()
api_instance = client.CoreV1Api()


class NameSpace:
    def __init__(self):
        pass

    def get(self, name):
        try:
            api_response = api_instance.read_namespace(name=name)
            return api_response
        except ApiException as e:
            status = e.status
            reason = e.reason
            reason = "Failed to get namespace {}.\n Reason: {}".format(name, reason)
            raise AdminServiceException(status=status, reason=reason)

    def create(self, name):
        try:
            body = {
                'kind': 'Namespace',
                'apiVersion': 'v1',
                'metadata': {
                    'name': name,
                }
            }
            api_response = api_instance.create_namespace(body=body)
        except ApiException as e:
            status = e.status
            reason = e.reason
            reason = "Failed to get namespace {}.\n Reason: {}".format(name, reason)
            raise AdminServiceException(status=status, reason=reason)


class ServiceAccount:
    def __init__(self):
        pass

    def get(self, name):
        try:
            api_response = api_instance.read_namespaced_service_account(name=name, namespace=name)
            return api_response
        except ApiException as e:
            status = e.status
            reason = e.reason
            reason = "Failed to get namespace {}.\n Reason: {}".format(name, reason)
            raise AdminServiceException(status=status, reason=reason)

    def create(self, name):
        try:
            body = {
                'kind': 'ServiceAccount',
                'apiVersion': 'v1',
                'metadata': {
                    'name': name,
                    'namespace': name
                },
            }
            api_response = api_instance.create_namespaced_service_account(namespace=name, body=body)
        except ApiException as e:
            status = e.status
            reason = e.reason
            reason = "Failed to get namespace {}.\n Reason: {}".format(name, reason)
            raise AdminServiceException(status=status, reason=reason)


class Secret:
    def __init__(self):
        pass

    def get(self, name, namespace):
        try:
            api_response = api_instance.read_namespaced_secret(name=name, namespace=namespace)
            return api_response
        except ApiException as e:
            status = e.status
            reason = e.reason
            reason = "Failed to get namespace {}.\n Reason: {}".format(name, reason)
            raise AdminServiceException(status=status, reason=reason)


def get_token(user):
    ns_helper = NameSpace()
    sa_helper = ServiceAccount()
    secret_helper = Secret()
    try:
        ns_helper.get(user)
    except AdminServiceException as e:
        if e.status == 404:
            ns_helper.create(user)
        else:
            raise e
    try:
        sa_helper.get(user)
    except AdminServiceException as e:
        if e.status == 404:
            sa_helper.create(user)
        else:
            raise e
    retry = 10
    i = 0
    while True:
        sa_obj = sa_helper.get(user)
        secrets = sa_obj.secrets
        print(secrets)
        if i >= retry:
            break
        if secrets is None:
            time.sleep(0.5)
            i += 1
            continue
        else:
            break
    secrets = sa_obj.secrets
    if secrets is None:
        reason = "Failed to get token for user {}".format(user)
        raise AdminServiceException(status=1001, reason=reason)
    secret = secrets[0].name
    secret_obj = secret_helper.get(secret, user)
    secret_token = 'Bearer ' + base64.b64decode(secret_obj.data["token"]).decode("utf-8")
    print(secret_token)
    return secret_token


class AdminServiceException(Exception):

    def __init__(self, status=None, reason=None):
        self.status = status
        self.reason = reason

    def __str__(self):
        error_message = "Reason: {0}\n".format(self.reason)
        return error_message

