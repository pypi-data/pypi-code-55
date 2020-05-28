# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collections
import logging
import socket
import threading
import typing
from enum import Enum

from opentelemetry.context import attach, detach, set_value
from opentelemetry.trace import DefaultSpan
from opentelemetry.util import time_ns
from opentelemetry.sdk.trace.export import Span, SpanProcessor, SpanExporter
from opentelemetry.aspecto.privacy_engine import PrivacyEngine

logger = logging.getLogger(__name__)
_ASPECTO_CLI_HEADER = '"x-origin":"aspecto-cli"'
_HEADERS_KEY = "http.request.headers"


class BatchExportSpanProcessor(SpanProcessor):
    """Batch span processor implementation.

    BatchExportSpanProcessor is an implementation of `SpanProcessor` that
    batches ended spans and pushes them to the configured `SpanExporter`.
    """

    _FLUSH_TOKEN_SPAN = DefaultSpan(context=None)

    def __init__(
        self,
        span_exporters: typing.List[SpanExporter] = None,
        tags: typing.Dict = None,
        max_queue_size: int = 2048,
        schedule_delay_millis: float = 5000,
        max_export_batch_size: int = 512,
    ):
        if span_exporters is None:
            span_exporters = []
        if tags is None:
            tags = {}

        if max_queue_size <= 0:
            raise ValueError("max_queue_size must be a positive integer.")

        if schedule_delay_millis <= 0:
            raise ValueError("schedule_delay_millis must be positive.")

        if max_export_batch_size <= 0:
            raise ValueError("max_export_batch_size must be a positive integer.")

        if max_export_batch_size > max_queue_size:
            raise ValueError(
                "max_export_batch_size must be less than and equal to max_export_batch_size."
            )

        self.tags = tags
        self.PrivacyEngine = None
        self.span_exporters = span_exporters
        self.queue = collections.deque([], max_queue_size)  # type: typing.Deque[Span]
        self.worker_thread = threading.Thread(target=self.worker, daemon=True)
        self.condition = threading.Condition(threading.Lock())
        self.flush_condition = threading.Condition(threading.Lock())
        # flag to indicate that there is a flush operation on progress
        self._flushing = False
        self.schedule_delay_millis = schedule_delay_millis
        self.max_export_batch_size = max_export_batch_size
        self.max_queue_size = max_queue_size
        self.done = False
        # flag that indicates that spans are being dropped
        self._spans_dropped = False
        # precallocated list to send spans to exporter
        self.spans_list = [
            None
        ] * self.max_export_batch_size  # type: typing.List[typing.Optional[Span]]
        self.worker_thread.start()

    def add_exporter(self, exporter: SpanExporter):
        self.span_exporters.append(exporter)

    def init_privacy_engine(self, privacy_rules):
        self.PrivacyEngine = PrivacyEngine(privacy_rules)

    def on_start(self, span: Span) -> None:
        # TODO: Remove when resource issue is fixed
        for tag, value in self.tags.items():
            span.set_attribute(tag, value)

    def on_end(self, span: Span) -> None:
        if self.done:
            logger.warning("Already shutdown, dropping span.")
            return
        if len(self.queue) == self.max_queue_size:
            if not self._spans_dropped:
                logger.warning("Queue is full, likely spans will be dropped.")
                self._spans_dropped = True
        if (
            _HEADERS_KEY in span.attributes
            and span.attributes[_HEADERS_KEY] is not None
            and _ASPECTO_CLI_HEADER in span.attributes[_HEADERS_KEY].lower()
        ):
            return

        if self.PrivacyEngine is None:
            print("Skipping trace since PrivacyEngine is None")
            return

        if self.PrivacyEngine.execute_rules(span):
            return

        self.queue.appendleft(span)

        if len(self.queue) >= self.max_queue_size // 2:
            with self.condition:
                self.condition.notify()

    def worker(self):
        timeout = self.schedule_delay_millis / 1e3
        while not self.done:
            if len(self.queue) < self.max_export_batch_size and not self._flushing:
                with self.condition:
                    self.condition.wait(timeout)
                    if not self.queue:
                        # spurious notification, let's wait again
                        continue
                    if self.done:
                        # missing spans will be sent when calling flush
                        break

            # subtract the duration of this export call to the next timeout
            start = time_ns()
            self.export()
            end = time_ns()
            duration = (end - start) / 1e9
            timeout = self.schedule_delay_millis / 1e3 - duration

        # be sure that all spans are sent
        self._drain_queue()

    def export(self) -> None:
        """Exports at most max_export_batch_size spans."""
        idx = 0
        notify_flush = False
        # currently only a single thread acts as consumer, so queue.pop() will
        # not raise an exception
        while idx < self.max_export_batch_size and self.queue:
            span = self.queue.pop()
            if span is self._FLUSH_TOKEN_SPAN:
                notify_flush = True
            else:
                self.spans_list[idx] = span
                idx += 1
        token = attach(set_value("suppress_instrumentation", True))
        try:
            # Ignore type b/c the Optional[None]+slicing is too "clever"
            # for mypy
            for exporter in self.span_exporters:
                exporter.export(self.spans_list[:idx])  # type: ignore
        # pylint: disable=broad-except
        except Exception:
            logger.exception("Exception while exporting Span batch.")
        detach(token)

        if notify_flush:
            with self.flush_condition:
                self.flush_condition.notify()

        # clean up list
        for index in range(idx):
            self.spans_list[index] = None

    def _drain_queue(self):
        """"Export all elements until queue is empty.

        Can only be called from the worker thread context because it invokes
        `export` that is not thread safe.
        """
        while self.queue:
            self.export()

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        if self.done:
            logger.warning("Already shutdown, ignoring call to force_flush().")
            return True

        self._flushing = True
        self.queue.appendleft(self._FLUSH_TOKEN_SPAN)

        # wake up worker thread
        with self.condition:
            self.condition.notify_all()

        # wait for token to be processed
        with self.flush_condition:
            ret = self.flush_condition.wait(timeout_millis / 1e3)

        self._flushing = False

        if not ret:
            logger.warning("Timeout was exceeded in force_flush().")
        return ret

    def shutdown(self) -> None:
        # signal the worker thread to finish and then wait for it
        self.done = True
        with self.condition:
            self.condition.notify_all()
        self.worker_thread.join()
        for exporter in self.span_exporters:
            exporter.shutdown()
