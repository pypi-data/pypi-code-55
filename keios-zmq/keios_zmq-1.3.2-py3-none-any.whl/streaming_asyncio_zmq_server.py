import asyncio
from asyncio import Queue, Task
from typing import Callable, List, AsyncGenerator

import aiozmq
import zmq

from keios_zmq.keios_message import KeiosMessage
from keios_zmq.log_provider import LogProvider
from keios_zmq.zmq_server import BulkMessage, ZMQServer
from keios_zmq.zmsg_assembly import ZMsgAssembly


class StreamingAsyncioZmqServer(ZMQServer):
    """
    This implementation offers server side streaming support

    Client                      Server
     _________
    | Request |                 ____________
    |_________|      ---->     | Stream:    |
                               |            |
                     <---      |  next      |
                               |            |
                     <---      |  next      |
                     <---      |  complete  |
                               |____________|


    """
    _log = LogProvider.get_logger("streaming-asyncio-keios-zmq-server")

    def __init__(self, port: int, dispatcher: Callable[[List[KeiosMessage]], AsyncGenerator[KeiosMessage, None]]):
        self._port = port
        self._dispatcher = dispatcher
        self._tasks: List[Task] = []

    async def start(self):
        router = await aiozmq.create_zmq_stream(zmq.ROUTER, bind="tcp://*:{}".format(self._port))
        queue = Queue()
        self._tasks.append(asyncio.create_task(self._inbound_task(router, queue)))
        self._tasks.append(asyncio.create_task(self._outbound_task(router, queue)))

    async def _outbound_task(self, router, outbound_queue: Queue):
        self._log.debug("Outbound task started")
        try:
            while True:
                bulk = await outbound_queue.get()
                outbound_queue.task_done()

                self._log.debug(f"Item is processed, sending response. {bulk.identifier}")
                router.write([bulk.identifier] + ZMsgAssembly.assemble(bulk.messages))
                self._log.debug("Written.")
        except asyncio.CancelledError as e:
            self._log.info("Outbound task cancelled")
            router.close()
            raise e

    async def _inbound_task(self, router, outbound_queue: Queue):
        self._log.debug("Inbound task started")
        try:
            while True:
                self._log.debug("Waiting for ze message")
                zmsg = await router.read()
                self._log.debug(f"Message received: {zmsg}")
                identity, items = self.destruct(zmsg)
                self._log.debug(f"Creating stream with identity: {identity}")
                await self._handle_message(BulkMessage(identity, items), outbound_queue)
        except asyncio.CancelledError as e:
            self._log.info("Inbound task cancelled")
            raise e

    async def stream_process(self, bulk: BulkMessage, outbound_queue: Queue):
        try:
            async for m in self._dispatcher(bulk.messages):
                self._log.debug("Stream[%s] sending message", bulk.identifier)
                await outbound_queue.put(BulkMessage(bulk.identifier, [m]))
                self._log.debug("Stream[%s] put on queue", bulk.identifier)
            await outbound_queue.put(
                BulkMessage(bulk.identifier, [KeiosMessage({'message_type': 'complete'}, bytes(0))]))
            self._log.debug("Stream[%s] completed", bulk.identifier)
        except asyncio.CancelledError as e:
            raise e
        except Exception as e:
            self._log.error("An error occurred:", e)
            await outbound_queue.put(
                BulkMessage(bulk.identifier, [KeiosMessage({'message_type': 'error'}, e.__str__().encode())]))

    async def _handle_message(self, bulk_message: BulkMessage, outbound_queue: Queue):
        if len(bulk_message.messages) == 1 and bulk_message.messages[0].header.get("type") == "HCheck":
            await outbound_queue.put(BulkMessage(bulk_message.identifier,
                                                 [KeiosMessage({'type': 'HCheck'}, bytes("pong", encoding="utf-8"))]))
            await outbound_queue.put(
                BulkMessage(bulk_message.identifier, [KeiosMessage({'message_type': 'complete'}, bytes(0))]))
        else:
            self._tasks.append(asyncio.create_task(self.stream_process(bulk_message, outbound_queue)))

    def start_server(self):
        self._log.info("Starting asyncio-keios-zmq-server on port %d", self._port)
        loop = asyncio.get_event_loop()
        loop.create_task(self.start())
        loop.run_forever()

    def close(self):
        self._log.info("Stopping server")
        for task in self._tasks:
            task.cancel()
        loop = asyncio.get_event_loop()
        loop.call_soon_threadsafe(loop.stop)
        loop.call_soon_threadsafe(loop.close)
        self._log.info("Stopped. bye.")
