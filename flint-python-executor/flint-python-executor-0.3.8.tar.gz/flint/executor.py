from flask import Flask, request, jsonify
from handler.handler_helper import Handler
from handler.flow_data import FlowDataException
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import os

application = Flask(__name__)
global_workflows = {}

config.load_kube_config()
api_instance = client.VersionApi()

class App:

    def __init__(self):
        pass

    def register_workflows(self, workflows):
        global global_workflows
        global_workflows = workflows

    @staticmethod
    @application.route('/execute')
    def execute():
        missing_args = []
        step = request.args.get('step', default=None)
        workflow = request.args.get('workflow', default=None)
        obj_name = request.args.get('obj_name', default=None)
        group = request.args.get('group', default=None)
        version = request.args.get('version', default=None)
        resource = request.args.get('resource', default=None)
        namespace = request.args.get('namespace', default=None)
        if step is None:
            missing_args.append("step")
        if workflow is None:
            missing_args.append("workflow")
        if obj_name is None:
            missing_args.append("workflow")
        if group is None:
            missing_args.append("group")
        if version is None:
            missing_args.append("version")
        if resource is None:
            missing_args.append("resource")
        if namespace is None:
            missing_args.append("namespace")
        if len(missing_args) > 0:
            message = "Flint Python Executor API Missing params: {}".format(', '.join(missing_args))
            response = {
                "message": message,
                "status": "failure"
            }
        else:
            handler_instance = Handler()
            handler_instance.flow_data.obj_name = obj_name
            handler_instance.flow_data.group = group
            handler_instance.flow_data.version = version
            handler_instance.flow_data.namespace = namespace
            handler_instance.flow_data.plural = resource
            try:
                global_workflows[workflow][step](handler_instance)
                response = {
                    "message": "",
                    "status": "success"
                }
            except FlowDataException as e:
                response = {
                    "message": e.reason,
                    "status": "failure"
                }
            except Exception as err:
                response = {
                    "message": repr(err),
                    "status": "failure"
                }
        return jsonify(response)

    @staticmethod
    @application.route('/health')
    def health():
        try:
            api_response = api_instance.get_code()
            response = {
                "status": "available"
            }
        except ApiException as e:
            response = {
                "status": "unavailable"
            }
        return jsonify(response)

    @staticmethod
    def start():
        try:
            debug = os.getenv("DEBUG")
            if debug == "true":
                application.config["DEBUG"] = True
                application.config["ENV"] = "development"
                application.run(host='0.0.0.0', port=8080)
            else:
                application.run(host='0.0.0.0', port=8080)

        except ExecutorException as e:
            raise ExecutorException(status=e.status, reason=e.reason)
        except Exception as e:
            print(e)
            raise ExecutorException(status=0, reason="Failed to start python executor api service")


def create_app():
    return App()


class ExecutorException(Exception):

    def __init__(self, status=None, reason=None):
        self.status = status
        self.reason = reason

    def __str__(self):
        error_message = "Reason: {0}\n".format(self.reason)
        return error_message
