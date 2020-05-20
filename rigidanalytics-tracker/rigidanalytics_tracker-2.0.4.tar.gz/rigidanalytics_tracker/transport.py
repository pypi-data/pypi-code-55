from datetime import datetime, timedelta
import json

import urllib3  # type: ignore

from ._types import MYPY
from .worker import BackgroundWorker


if MYPY:
    from typing import Any
    from typing import Optional

    from ._types import Event


POOL_MANAGER = urllib3.PoolManager(maxsize=20, block=True)


class Transport(object):
    """Baseclass for all transports.
    A transport is used to send an event to sentry.
    """

    def __init__(self, endpoint):
        # type: () -> None
        self.endpoint = endpoint

    def capture_event(
        self,
        event  # type: Event
    ):
        # type: (...) -> None
        """This gets invoked with the event dictionary when an event should
        be sent to sentry.
        """
        raise NotImplementedError()

    def flush(
        self,
        timeout,  # type: float
        callback=None,  # type: Optional[Any]
    ):
        # type: (...) -> None
        """Wait `timeout` seconds for the current events to be sent out."""
        pass

    def kill(self):
        # type: () -> None
        """Forcefully kills the transport."""
        pass

    def __del__(self):
        # type: () -> None
        try:
            self.kill()
        except Exception:
            pass


class HttpTransport(Transport):
    """The default HTTP transport."""

    def __init__(self, endpoint):
        # type: () -> None

        super(HttpTransport, self).__init__(endpoint)
        self._worker = BackgroundWorker()
        self._disabled_until = None  # type: Optional[datetime]
        self._retry = urllib3.util.Retry()

        self._pool = POOL_MANAGER

    def _preform_event_send(
        self,
        endpoint,
        event  # type: Event
    ):
        # type: (...) -> None
        if self._disabled_until is not None:
            if datetime.utcnow() < self._disabled_until:
                return
            self._disabled_until = None

        # print('Sending event: ')
        # print(event)

        response = self._send_event_request(self.endpoint, event)

        # print('Got response with status: ' + str(response.status))
        # print(response.data)

        try:
            if response.status == 429:
                self._disabled_until = datetime.utcnow() + timedelta(
                    seconds=self._retry.get_retry_after(response) or 60
                )
                return

            elif response.status >= 300 or response.status < 200:
                print(
                    "Unexpected status code: %s (body: %s)",
                    response.status,
                    response.data,
                )
        finally:
            response.close()

        self._disabled_until = None

    def _send_event_request(
            self,
            endpoint,  # type: str
            event,  # type: Event
    ):
        encoded_data = json.dumps(event).encode('utf-8')
        response = self._pool.request(
            "POST",
            endpoint,
            body=encoded_data,
            headers={'Content-Type': 'application/json'})

        return response

    def capture_event(
        self,
        event  # type: Event
    ):
        # type: (...) -> None

        def send_event_wrapper():
            # type: () -> None
            self._preform_event_send(self.endpoint, event)

        self._worker.submit(send_event_wrapper)

    def flush(
        self,
        timeout,  # type: float
        callback=None,  # type: Optional[Any]
    ):
        # type: (...) -> None
        print("Flushing HTTP transport")
        if timeout > 0:
            self._worker.flush(timeout, callback)

    def kill(self):
        # type: () -> None
        print("Killing HTTP transport")
        self._worker.kill()


def make_transport(endpoint):
    # type: () -> Transport
    return HttpTransport(endpoint)
