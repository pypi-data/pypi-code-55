import copy
import json
import threading
import time

from securenative.config.securenative_options import SecureNativeOptions
from securenative.exceptions.securenative_http_exception import SecureNativeHttpException
from securenative.http.securenative_http_client import SecureNativeHttpClient
from securenative.logger import Logger


class QueueItem:
    def __init__(self, url, body, retry):
        self.url = url
        self.body = body
        self.retry = retry


class EventManager:
    def __init__(self, options=SecureNativeOptions(), http_client=None):
        if options.api_key is None:
            raise ValueError('API key cannot be None, please get your API key from SecureNative console.')

        if not http_client:
            self.http_client = SecureNativeHttpClient(options)
        else:
            self.http_client = http_client

        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

        self.options = options
        self.queue = list()
        self.send_enabled = False
        self.attempt = 0
        self.coefficients = [1, 1, 2, 3, 5, 8, 13]
        self.thread = None
        self.interval = options.interval

    def send_async(self, event, resource_path):
        if self.options.disable:
            Logger.warning("SDK is disabled. no operation will be performed")
            return

        item = QueueItem(
            resource_path,
            json.dumps(EventManager.serialize(event)),
            False
        )

        self.queue.append(item)
        if self._is_queue_full():
            self.queue = self.queue[:len(self.queue - 1)]

    def flush(self):
        queue_copy = copy.copy(self.queue)
        self.queue = list()

        for item in queue_copy:
            self.http_client.post(item.url, item.body)

    def send_sync(self, event, resource_path, retry):
        if self.options.disable:
            Logger.warning("SDK is disabled. no operation will be performed")
            return

        Logger.debug("Attempting to send event {}".format(event))
        res = self.http_client.post(
            resource_path,
            json.dumps(EventManager.serialize(event))
        )
        if res.status_code != 200:
            Logger.info("SecureNative failed to call endpoint {} with event {}. adding back to queue".format(
                resource_path, event))
            item = QueueItem(
                resource_path,
                json.dumps(EventManager.serialize(event)),
                retry
            )
            self.queue.append(0, item)
            if self._is_queue_full():
                self.queue = self.queue[:len(self.queue - 1)]
        return res

    def _is_queue_full(self):
        return len(self.queue) > self.options.max_events

    def run(self):
        while True:
            if len(self.queue) > 0 and self.send_enabled:
                for item in self.queue:
                    try:
                        res = self.http_client.post(item.url, item.body)
                        if res.status_code is 401:
                            item.retry = False
                        elif res.status_code != 200:
                            raise SecureNativeHttpException(res.status_code)

                        Logger.debug("Event successfully sent; {}".format(item.body))
                        self.queue.remove(item)
                        return res
                    except Exception as e:
                        Logger.error("Failed to send event; {}".format(e))
                        if item.retry:
                            if len(self.coefficients) == self.attempt + 1:
                                self.attempt = 0

                            back_off = self.coefficients[self.attempt] * self.options.interval
                            Logger.debug("Automatic back-off of {}".format(back_off))
                            self.send_enabled = False
                            time.sleep(back_off)
                            self.send_enabled = True
                        else:
                            self.queue.remove(item)
                time.sleep(self.interval/1000)

    def start_event_persist(self):
        Logger.debug("Starting automatic event persistence")
        if self.options.auto_send or self.send_enabled:
            self.send_enabled = True
        else:
            Logger.debug("Automatic event persistence is disabled, you should persist events manually")

    def stop_event_persist(self):
        if self.send_enabled:
            Logger.debug("Attempting to stop automatic event persistence")
            try:
                if self.thread:
                    self.thread.stop()
            except ValueError as e:
                Logger.error("Could not stop event scheduler; {}".format(e))

            Logger.debug("Stopped event persistence")

    @staticmethod
    def serialize(obj):
        return {
            "rid": obj.rid,
            "eventType": obj.event_type.value,
            "userId": obj.user_id,
            "userTraits": {
                "name": obj.user_traits.name,
                "email": obj.user_traits.email,
                "createdAt": obj.user_traits.created_at,
            },
            "request": {
                "cid": obj.request.cid,
                "vid": obj.request.vid,
                "fp": obj.request.fp,
                "ip": obj.request.ip,
                "remoteIp": obj.request.remote_ip,
                "method": obj.request.method,
                "url": obj.request.url,
                "headers": obj.request.headers
            },
            "timestamp": obj.timestamp,
            "properties": obj.properties,
        }
