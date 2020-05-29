from subprocess import Popen
import string
import random
import logging
import kubernetes
from plynx.constants import JobReturnStatus, ParameterTypes
from plynx.db.node import Parameter
import plynx.plugins.executors.local as local


NAMESPACE = 'test'

def gen_rand(length=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def gen_rand_name():
    return '{}-{}'.format('job', gen_rand())


def _extend_default_node_in_place(node):
    node.parameters.extend(
        [
            Parameter.from_dict({
                'name': '_image',
                'parameter_type': ParameterTypes.STR,
                'value': 'alpine:3.7',
                'mutable_type': False,
                'publicable': True,
                'removable': False,
                }
            ),
        ]
    )


def get_param_dict(node):
    res = {}
    for parameter in node.parameters:
        res[parameter.name] = parameter.value
    return res

_api_instance = None

def get_api_instance():
    global _api_instance
    if _api_instance:
        return _api_instance
    kubernetes.config.load_kube_config()
    configuration = kubernetes.client.Configuration()
    _api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
    return _api_instance


def create_kubernetes_body(node_param_dict, workdir):
    job_name = gen_rand_name()
    container_image = node_param_dict['_image']
    ENV_LIST = []

    body = kubernetes.client.V1Pod(api_version="v1", kind="Pod")
    body.metadata = kubernetes.client.V1ObjectMeta(namespace=NAMESPACE, name=job_name)
    body.status = kubernetes.client.V1PodStatus()

    # Now we start with the Template...
    template = kubernetes.client.V1PodTemplate()
    template.template = kubernetes.client.V1PodTemplateSpec()

    container = kubernetes.client.V1Container(
        name=job_name,
        image=container_image,
        env=ENV_LIST,
        command=['ls', '/plynx'],
        working_dir=workdir,
    )
    template.template.spec = kubernetes.client.V1PodSpec(
        containers=[container],
        restart_policy='Never',
        )
    # And finaly we can create our V1JobSpec!
    #body.spec = kubernetes.client.V1JobSpec(ttl_seconds_after_finished=600, template=template.template)
    body.spec = kubernetes.client.V1PodSpec(
        containers=[container],
        restart_policy='Never',
        )

    return body


class BashJinja2(local.BashJinja2):
    @classmethod
    def get_default_node(cls, is_workflow):
        node = super().get_default_node(is_workflow)
        _extend_default_node_in_place(node)
        return node

    def exec_script(self, script_location, command='bash'):
        res = JobReturnStatus.SUCCESS

        try:

            body = create_kubernetes_body(get_param_dict(self.node), self.workdir)
            api_response = get_api_instance().create_namespaced_pod(NAMESPACE, body, pretty=True)

        except Exception as e:
            res = JobReturnStatus.FAILED
            logging.exception("Job failed")
            with open(self.logs['worker'], 'a+') as worker_log_file:
                worker_log_file.write(self._make_debug_text("JOB FAILED"))
                worker_log_file.write(str(e))

        return res


class PythonNode(local.PythonNode):
    @classmethod
    def get_default_node(cls, is_workflow):
        node = super().get_default_node(is_workflow)
        _extend_default_node_in_place(node)
        return node
