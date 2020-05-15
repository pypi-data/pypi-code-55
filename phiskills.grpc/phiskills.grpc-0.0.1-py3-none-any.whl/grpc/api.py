import argparse
import os
import signal
import sys
from concurrent import futures
from enum import Enum

import grpc
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2_grpc
from grpc_health.v1.health_pb2 import HealthCheckResponse

GRPC_PORT = 50051


class Status(Enum):
    UNKNOWN = HealthCheckResponse.UNKNOWN
    SERVING = HealthCheckResponse.SERVING
    NOT_SERVING = HealthCheckResponse.NOT_SERVING

    def __str__(self):
        return self.name


class Api:
    def __init__(self, name: str, max_workers: int = 10):
        self.name = name
        self.port = GRPC_PORT
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
        self.healthServer = health.HealthServicer()
        health_pb2_grpc.add_HealthServicer_to_server(
            self.healthServer,
            self.server
        )
        self.status = Status.UNKNOWN

    def use_params(self) -> None:
        self.__parse_env()
        self.__parse_flag()

    def use_port(self, port: int) -> None:
        self.port = port

    def start(self) -> None:
        self.server.add_insecure_port(f'[::]:{self.port}')
        self.server.start()
        self.activate()

    def stop(self, grace: int = 60) -> None:
        self.healthServer.enter_graceful_shutdown()
        self.server.stop(grace)
        self.deactivate()

    def activate(self) -> None:
        self.__update_status(Status.SERVING)

    def deactivate(self) -> None:
        self.__update_status(Status.NOT_SERVING)

    def wait_for_termination(self, grace: int = 60) -> None:
        def signal_handler(_sig, _frame):
            print(f'Termination requested: max {grace}s left')
            self.server.stop(grace)
            print(f'{self.name} server terminated')
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.pause()
        self.server.wait_for_termination()

    def __update_status(self, status: Status) -> None:
        self.healthServer.set(self.name, status.value)
        self.status = status

    def __parse_flag(self) -> None:
        parser = argparse.ArgumentParser(description=f'{self.name} gRPC API Server')
        parser.add_argument('--port', type=int, default=0, help='custom port')
        port = parser.parse_args().port
        if port != 0:
            self.port = port

    def __parse_env(self) -> None:
        try:
            port = int(os.environ.get('PORT'))
            if port != 0:
                self.port = port
        except (TypeError, ValueError):
            return
