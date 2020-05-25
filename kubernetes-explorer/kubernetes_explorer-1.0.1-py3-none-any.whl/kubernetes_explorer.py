from enum import Enum
import logging

from kubernetes import client, config
from kubernetes.client.rest import ApiException


class KubernetesObject(Enum):
    DEPLOYMENT = 'deployment'
    NAMESPACE = 'namespace'
    POD = 'pod'
    SECRET = 'secret'
    SERVICE = 'service'


class KubernetesExplorer:
    def __init__(self, context=None):
        config.load_kube_config(context=context)
        self.api = client.CoreV1Api()
        self.apps_api = client.AppsV1Api()
        self.logger = logging.getLogger('kubernetes-explorer')

    def get_pods(self, namespace: str = None):
        try:
            if namespace is not None:
                return self.api.list_namespaced_pod(namespace).items
            else:
                return self.api.list_pod_for_all_namespaces().items
        except ApiException as e:
            self.log_error(e)

        return []

    def get_services(self, namespace: str = None):
        try:
            if namespace is not None:
                return self.api.list_namespaced_service(namespace).items
            else:
                return self.api.list_service_for_all_namespaces().items
        except ApiException as e:
            self.log_error(e)

        return []

    def get_secrets(self, namespace: str = None):
        try:
            if namespace is not None:
                return self.api.list_namespaced_secret(namespace).items
            else:
                return self.api.list_secret_for_all_namespaces().items
        except ApiException as e:
            self.log_error(e)

        return []

    def get_deployments(self, namespace: str = None):
        try:
            if namespace is not None:
                return self.apps_api.list_namespaced_deployment(namespace).items
            else:
                return self.apps_api.list_deployment_for_all_namespaces().items
        except ApiException as e:
            self.log_error(e)

        return []

    def get_namespaces(self, namespace: str = None):
        try:
            if namespace is not None:
                return [self.api.read_namespace(namespace)]
            else:
                return self.api.list_namespace().items
        except ApiException as e:
            self.log_error(e)

        return []

    def log_error(self, e: ApiException):
        self.logger.error(
            f'Error while contacting Kubernetes API: {e.reason} ({e.status})')
        exit(1)
