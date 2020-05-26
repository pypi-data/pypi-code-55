import asyncio
import queue
from asyncio import Queue
from typing import Generator, Callable, List

import aiozmq
import zmq

from keios_zmq.keios_message import KeiosMessage
from keios_zmq.log_provider import LogProvider
from keios_zmq.streaming_dispatcher import StreamingDispatcher
from keios_zmq.zmq_server import BulkMessage, ZMQServer, PoisonPill
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

    def __init__(self, port: int, dispatcher: StreamingDispatcher):
        self._port = port
        self._dispatcher = dispatcher
        self._queue = queue.Queue()

    async def start(self, loop):
        router = await aiozmq.create_zmq_stream(zmq.ROUTER, bind="tcp://*:{}".format(self._port))
        loop.create_task(self._inbound_task(loop, router, self._queue))
        loop.run_in_executor(None, self._outbound_task, router, self._queue)

    def _outbound_task(self, router, outbound_queue: queue.Queue):
        while True:
            bulk = outbound_queue.get()
            outbound_queue.task_done()

            if type(bulk) == PoisonPill:
                break

            self._log.info(f"Item is processed, sending response. {bulk.identifier}")
            router.write([bulk.identifier] + ZMsgAssembly.assemble(bulk.messages))
            self._log.info("Written.")
        self._log.info("Received poison pill - closing")
        router.close()

    async def _inbound_task(self, loop, router, outbound_queue: Queue):
        while True:
            zmsg = await router.read()
            self._log.debug(f"Message received: {zmsg}")
            identity, items = self.destruct(zmsg)
            self._log.debug(f"Creating stream with identity: {identity}")
            loop.run_in_executor(None, self.stream_process, BulkMessage(identity, items), outbound_queue)

    def stream_process(self, bulk: BulkMessage, outbound_queue: Queue):
        try:
            for m in self._dispatcher.execute(bulk.messages):
                self._log.info("Stream[%s] sending message", bulk.identifier)
                outbound_queue.put(BulkMessage(bulk.identifier, [m]))
                self._log.info("Stream[%s] put on queue", bulk.identifier)
            outbound_queue.put(BulkMessage(bulk.identifier, [KeiosMessage({'message_type': 'complete'}, bytes(0))]))
            self._log.info("Stream[%s] completed", bulk.identifier)
        except Exception as e:
            self._log.error("An error occurred:", e)
            outbound_queue.put(
                BulkMessage(bulk.identifier, [KeiosMessage({'message_type': 'error'}, e.__str__().encode())]))

    def start_server(self):
        self._log.info("Starting asyncio-keios-zmq-server on port %d", self._port)
        loop = asyncio.get_event_loop()
        loop.create_task(self.start(loop))
        loop.run_forever()

    def close(self):
        self._log.info("Stopping server")
        # send a poison pill to stop the executor based outbound task
        self._queue.put(PoisonPill(bytes(), []))

        loop = asyncio.get_event_loop()
        loop.call_soon_threadsafe(loop.stop)
        loop.call_soon_threadsafe(loop.close)
        self._log.info("Stopped. bye.")
