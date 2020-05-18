from concurrent import futures
import grpc
import asyncio
import sys, inspect

import health_pb2
import health_pb2_grpc
import plugin_pb2_grpc
import health

from factory import NodeFactory
from node import NodeServicer, Node
from runtime import Runtime
from spec import Spec


async def start():

    if len(sys.argv) > 3 and sys.argv[1] == '-s':
        Spec.generate(sys.argv[2], sys.argv[3])
        return

    init()

    healthServicer = health.HealthServicer()
    healthServicer.set_status("plugin", 1)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    health_pb2_grpc.add_HealthServicer_to_server(healthServicer, server)
    plugin_pb2_grpc.add_NodeServicer_to_server(NodeServicer(), server)

    port = server.add_insecure_port('[::]:0')
    server.start()

    print("1|1|tcp|127.0.0.1:%d|grpc\n" % port, flush=True)

    Runtime.event.wait()


def init():
    frm = inspect.stack()[2]
    mod = inspect.getmodule(frm[0])
    clsmembers = inspect.getmembers(sys.modules[mod.__name__], inspect.isclass)
    for c in clsmembers:
        if issubclass(c[1], Node) and c[1] is not Node:
            cls = c[1]
            name = cls().id
            factory = NodeFactory(cls)
            Runtime.create_node(name, factory)
