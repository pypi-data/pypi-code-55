# -*- encoding: utf-8 -*-
import logging

from ddtrace import compat
from ddtrace.profiling import _attr
from ddtrace.profiling import _periodic
from ddtrace.profiling import _traceback
from ddtrace.profiling import exporter
from ddtrace.vendor import attr

LOG = logging.getLogger(__name__)


@attr.s
class Scheduler(_periodic.PeriodicService):
    """Schedule export of recorded data."""

    recorder = attr.ib()
    exporters = attr.ib()
    _interval = attr.ib(factory=_attr.from_env("DD_PROFILING_UPLOAD_INTERVAL", 60, float))
    _last_export = attr.ib(init=False, default=None)

    def start(self):
        """Start the scheduler."""
        LOG.debug("Starting scheduler")
        super(Scheduler, self).start()
        self._last_export = compat.time_ns()
        LOG.debug("Scheduler started")

    def flush(self):
        """Flush events from recorder to exporters."""
        LOG.debug("Flushing events")
        if self.exporters:
            events = self.recorder.reset()
            start = self._last_export
            self._last_export = compat.time_ns()
            total_events = sum(len(v) for v in events.values())
            for exp in self.exporters:
                try:
                    exp.export(events, start, self._last_export)
                except exporter.ExportError as e:
                    LOG.error("Unable to export %d events: %s", total_events, _traceback.format_exception(e))
                except Exception:
                    LOG.exception("Error while exporting %d events", total_events)

    periodic = flush
    on_shutdown = flush
