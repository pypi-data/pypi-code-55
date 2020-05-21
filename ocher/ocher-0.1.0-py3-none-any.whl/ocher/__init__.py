import json
import queue as Q
import sys
from dataclasses import dataclass
from typing import Iterator, Tuple, Any, Optional

import grpc

from .pb import ocher_pb2 as pb
from .pb import ocher_pb2_grpc as rpc


class Error(Exception):
    pass


@dataclass()
class Task:
    id: int
    queue: str
    args: bytes

    def __repr__(self):
        return f'Task<{self.id}:{self.queue}>'

    def json(self) -> Any:
        return json.loads(self.args)


class Transmitter:

    def __init__(self, id_: str, queue: str):
        self.__output = Q.Queue()
        self.__output.put(pb.Status(init=pb.Status.Init(id=id_, queue=queue)))
        self.__logger = None

    def __iter__(self) -> Iterator[pb.Status]:
        while True:
            item = self.__output.get()
            if item is None:
                break
            print('sending', item)
            yield item

    def finish(self, result: bytes = b""):
        self.__output.put(
            pb.Status(finish=pb.Status.Finish(result=result))
        )

    def error(self, message: str, error: Optional[bytes] = None):
        err = pb.Status.Error(message=message)
        if error:
            err.error = error
        status = pb.Status(error=err)
        self.__output.put(status)

    def cleanup(self):
        try:
            while True:
                self.__output.get_nowait()
        except Q.Empty:
            pass


class Client:

    def __init__(self, url: str, id_: str):
        self.id = id_
        channel = grpc.insecure_channel(url)
        self.__stub = rpc.OcherStub(channel)

    def tasks(self, *, queue: str) -> Iterator[Tuple[Transmitter, Task]]:
        try:
            tx = Transmitter(self.id, queue)
            stream = self.__stub.QueueTransactional(iter(tx))

            for t in stream:
                task = Task(id=t.id, queue=t.queue, args=t.args)
                yield tx, task

        except grpc.RpcError as exc:
            status_code = exc.code()

            if status_code == grpc.StatusCode.UNKNOWN:
                print(exc.details(), file=sys.stderr)
                return

            if status_code == grpc.StatusCode.UNAVAILABLE:
                raise Error("Service unavailable") from None
