import queue
import time
from threading import Thread

SLAVE_QUEUE_BUFFER_MAX_SIZE = 100

DEFAULT_SLEEP_DURATION = 1


class MessageQueue:

    def __init__(self, producer, consumer):
        assert isinstance(producer, MessageQueueWorker)
        assert isinstance(consumer, MessageQueueWorker)
        assert producer != consumer
        self.queue = queue.Queue(SLAVE_QUEUE_BUFFER_MAX_SIZE)
        self.producer = producer
        self.consumer = consumer

        self.producer.set_queue(self.queue)
        self.consumer.set_queue(self.queue)

    def start(self):
        self.producer.start()
        self.consumer.start()

    def stop(self):
        self.producer.stop_working()
        self.consumer.stop_working()


class MessageQueueWorker(Thread):

    def __init__(self, sleep_duration=DEFAULT_SLEEP_DURATION):
        super(MessageQueueWorker, self).__init__()
        self._queue = None
        self.sleep_duration = sleep_duration
        self.is_running = True

    def set_queue(self, q):
        assert isinstance(q, queue.Queue)
        self._queue = q

    def run(self):
        while self.is_running:
            if not self.do_work():
                continue
            time.sleep(self.sleep_duration)

    def is_queue_full(self):
        return self._queue.full()

    def is_empty_queue(self):
        return self._queue.empty()

    def put_message(self, msg):
        self._queue.put(msg)

    def get_next_message(self):
        return self._queue.get()

    # return True if works with queue items has finished and thread can sleep
    def do_work(self) -> bool:
        pass

    def stop_working(self):
        self.is_running = False