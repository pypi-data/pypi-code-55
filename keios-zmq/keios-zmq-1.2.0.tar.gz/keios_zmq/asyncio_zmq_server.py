import asyncio
from asyncio import Queue

import aiozmq
import zmq
from keios_zmq.dispatcher import Dispatcher
from keios_zmq.log_provider import LogProvider
from keios_zmq.zmq_server import ZMQServer, BulkMessage
from keios_zmq.zmsg_assembly import ZMsgAssembly


class AsyncioKeiosZMQ(ZMQServer):
    log = LogProvider.get_logger("asyncio-keios-zmq-server")

    def __init__(self, port: int, dispatcher: Dispatcher):
        self._port = port
        self._message_handler = dispatcher

    async def start(self, loop):
        task_queue = Queue()
        router = await aiozmq.create_zmq_stream(zmq.ROUTER, bind="tcp://*:{}".format(self._port))
        loop.create_task(self._inbound_task(loop, router, task_queue))
        loop.create_task(self._outbound_task(router, task_queue))

    async def _outbound_task(self, router, q: Queue):
        while True:
            item = await q.get()
            q.task_done()

            if item.done():
                bulk: BulkMessage = item.result()
                self.log.debug(f"Item is processed, sending response. {bulk.identifier}")
                router.write([bulk.identifier] + ZMsgAssembly.assemble(bulk.messages))
            else:
                self.log.debug("Item is not done, put item back to the queue")
                # put back on the queue if not done processing
                await asyncio.sleep(0.001)
                await q.put(item)

    async def _inbound_task(self, loop, router, q: Queue):
        while True:
            zmsg = await router.read()
            self.log.debug(f"Message received: {zmsg}")
            identity, items = self.destruct(zmsg)
            self.log.debug(f"Creating task with identity: {identity}")
            task = asyncio.create_task(self.process(loop, BulkMessage(identity, items)))
            await q.put(task)
            self.log.debug(f"Task put on queue with identity {identity}")

    async def process(self, loop, bulk: BulkMessage):
        self.log.debug("Processing message")
        result = await loop.run_in_executor(None, self._message_handler.execute, bulk.messages)
        self.log.debug(f"Done processing  {bulk.identifier}")
        return BulkMessage(bulk.identifier, result)

    def start_server(self):
        self.log.info("Starting asyncio-keios-zmq-server on port %d", self._port)
        loop = asyncio.get_event_loop()
        loop.create_task(self.start(loop))
        loop.run_forever()

    def close(self):
        self.log.info("Stopping server")
        loop = asyncio.get_running_loop()
        loop.stop()
        loop.close()
        self.log.info("Stopped. bye.")
