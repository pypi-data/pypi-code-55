import grpc
import plugin_pb2
import plugin_pb2_grpc
import sys

from asyncio import base_futures
from runtime import Runtime


class Node:
    def __init__(self):
        self.guid = ''
        self.name = ''
        self.delayBefore = 0.0
        self.delayAfter = 0.0
        self.continueOnError = False
        self.scope = ''

    def on_create(self, config: bytes):
        pass

    def on_message(self, in_message: bytes) -> bytes:
        pass

    def on_close(self):
        pass


class NodeServicer(plugin_pb2_grpc.NodeServicer):
    def Init(self, request: plugin_pb2.InitRequest, context):
        channel = grpc.insecure_channel('127.0.0.1:%d' % request.port)
        client = plugin_pb2_grpc.RuntimeHelperStub(channel)
        Runtime.set_client(client=client)

        return plugin_pb2.Empty()

    def OnCreate(self, request: plugin_pb2.OnCreateRequest, context):
        Runtime.active_nodes += 1

        config = request.config
        Runtime.factories[request.name].on_create(config)

        return plugin_pb2.OnCreateResponse()

    def OnMessage(self, request: plugin_pb2.OnMessageRequest, context):
        data = Runtime.decompress(request.inMessage)

        out_message = bytes()
        if request.guid in Runtime.nodes:
            out_message = Runtime.nodes[request.guid].on_message(data)

        return plugin_pb2.OnMessageResponse(outMessage=out_message)

    def OnClose(self, request: plugin_pb2.OnCloseRequest, context):
        if request.guid in Runtime.nodes:
            Runtime.nodes[request.guid].on_close()

        Runtime.active_nodes -= 1
        if Runtime.active_nodes <= 0:
            Runtime.event.set()

        return plugin_pb2.OnCloseResponse()
