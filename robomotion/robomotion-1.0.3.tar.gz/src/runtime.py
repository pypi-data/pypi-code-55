import gzip
import plugin_pb2
import json
import threading
from google.protobuf import json_format
from struct_pb2 import Struct

from plugin_pb2_grpc import RuntimeHelperStub

from types import SimpleNamespace as Namespace


class Variable:
    def __init__(self, scope: str, name: str):
        self.scope = scope
        self.name = name


class Runtime:
    active_nodes = 0
    client: RuntimeHelperStub = None
    event: threading.Event = threading.Event()
    factories = {}
    nodes = {}

    @staticmethod
    def set_client(client: RuntimeHelperStub):
        Runtime.client = client

    @staticmethod
    def create_node(name: str, factory):
        Runtime.factories[name] = factory

    @staticmethod
    def add_node(guid: str, node):
        Runtime.nodes[guid] = node

    @staticmethod
    def compress(data: bytes):
        return gzip.compress(data)

    @staticmethod
    def decompress(data: bytes):
        return gzip.decompress(data)

    @staticmethod
    def deserialize(data: bytes, c):
        node = c()
        obj = json.loads(data, object_hook=lambda d: Namespace(**d))
        for key in obj.__dict__.keys():
            node.__setattr__(key, obj.__dict__[key])
        return node

    @staticmethod
    def close():
        if Runtime.client is None:
            return

        request = plugin_pb2.Empty()
        Runtime.client.Close(request)

    @staticmethod
    def get_vault_item(vault_id: str, item_id: str):
        if Runtime.client is None:
            return {}

        request = plugin_pb2.GetVaultItemRequest(vaultId=vault_id, ItemId=item_id)
        response = Runtime.client.GetVaultItem(request)
        return json_format.MessageToDict(response.item)['value']

    @staticmethod
    def get_int_variable(variable: Variable, message: bytes):
        if Runtime.client is None:
            return 0

        var = plugin_pb2.Variable(scope=variable.scope, name=variable.name)
        request = plugin_pb2.GetVariableRequest(variable=var, message=message)
        response = Runtime.client.GetIntVariable(request)
        return response.value

    @staticmethod
    def get_string_variable(variable: Variable, message: bytes):
        if Runtime.client is None:
            return ""

        var = plugin_pb2.Variable(scope=variable.scope, name=variable.name)
        request = plugin_pb2.GetVariableRequest(variable=var, message=message)
        response = Runtime.client.GetStringVariable(request)
        return response.value

    @staticmethod
    def get_interface_variable(variable: Variable, message: bytes):
        if Runtime.client is None:
            return None

        var = plugin_pb2.Variable(scope=variable.scope, name=variable.name)
        request = plugin_pb2.GetVariableRequest(variable=var, message=message)
        response = Runtime.client.GetInterfaceVariable(request)

        return json_format.MessageToDict(response.value)['value']

    @staticmethod
    def set_int_variable(variable: Variable, message: bytes, value: int):
        if Runtime.client is None:
            return message

        var = plugin_pb2.Variable(scope=variable.scope, name=variable.name)
        request = plugin_pb2.SetIntVariableRequest(variable=var, message=message, value=value)
        response = Runtime.client.SetIntVariable(request)
        return response.message

    @staticmethod
    def set_string_variable(variable: Variable, message: bytes, value: str):
        if Runtime.client is None:
            return message

        var = plugin_pb2.Variable(scope=variable.scope, name=variable.name)
        request = plugin_pb2.SetStringVariableRequest(variable=var, message=message, value=value)
        response = Runtime.client.SetStringVariable(request)
        return response.message

    @staticmethod
    def set_interface_variable(variable: Variable, message: bytes, value: object):
        if Runtime.client is None:
            return message

        val = Struct()
        val.update({'value': value})

        var = plugin_pb2.Variable(scope=variable.scope, name=variable.name)
        request = plugin_pb2.SetInterfaceVariableRequest(variable=var, message=message, value=val)
        response = Runtime.client.SetInterfaceVariable(request)
        return response.message
