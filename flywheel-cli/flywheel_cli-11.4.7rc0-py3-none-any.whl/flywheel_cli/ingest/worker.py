"""Provides IngestWorker class."""
import copy
import logging
import multiprocessing
import time
import signal

from .client import DBClient
from .config import WorkerConfig
from .tasks import create_task
from . import errors

log = logging.getLogger(__name__)


class WorkerPool:
    """Ingest worker pool"""

    def __init__(self, worker_config: WorkerConfig):
        self._worker_config = worker_config
        self._processes = []
        self._running = False

    def start(self):
        """Start the worker with N processes. Noop if the worker already started."""
        if self._running:
            return

        self._running = True
        for _ in range(self._worker_config.jobs):
            self._start_single_worker()

    def _start_single_worker(self):
        """Start a worker process."""
        p_name = f"{self._worker_config.worker_name}-{len(self._processes)}"
        shutdown_event = multiprocessing.Event()
        target = Worker(self._worker_config, p_name, shutdown_event).run
        proc = multiprocessing.Process(target=target, name=p_name, daemon=True)
        proc.start()
        self._processes.append((proc, shutdown_event))

    def join(self):
        """Wait until all worker processes terminate"""
        for proc, _ in self._processes:
            proc.join()

    def shutdown(self):
        """Shutdown the executor.

        Send shutdown event for every worker processes and wait until all of them terminate.
        """
        for _, shutdown_event in self._processes:
            shutdown_event.set()
        self.join()


class Worker:  # pylint: disable=too-few-public-methods
    """Ingest worker, wait for task and execute it"""

    def __init__(self, config: WorkerConfig, name=None, shutdown=None):
        self.db = DBClient(config.db_url)  # pylint: disable=C0103
        self.config = config
        self.name = name or config.worker_name
        self.shutdown = shutdown or multiprocessing.Event()

    def run(self):
        """Run the worker"""
        orig_sigint_handler = signal.signal(signal.SIGINT, self.graceful_shutdown_handler)
        orig_sigterm_handler = signal.signal(signal.SIGTERM, self.graceful_shutdown_handler)
        orig_alarm_handler = signal.signal(signal.SIGALRM, alarm_handler)
        try:
            log.debug(f"{self.name} worker started, wating for connection...")
            self.wait_for_db()
            log.debug(f"{self.name} worker connected, waiting for tasks...")
            self.consume_tasks()
        finally:
            signal.signal(signal.SIGINT, orig_sigint_handler)
            signal.signal(signal.SIGTERM, orig_sigterm_handler)
            signal.signal(signal.SIGALRM, orig_alarm_handler)

    def consume_tasks(self):
        """Consume ingest tasks, do the actual work"""
        while not self.shutdown.is_set():
            next_task = ingest_db = None
            try:
                next_task = self.db.next_task(self.name)
                if not next_task:
                    time.sleep(self.config.sleep_time)
                    continue
                log.debug(f"{self.name} executing task {next_task}")
                ingest_db = copy.copy(self.db)
                ingest_db.bind(next_task.ingest_id)
                task = create_task(ingest_db, next_task, self.config)
                task.run()
                log.debug(f"{self.name} executing task completed {next_task}")
            except Exception:  # pylint: disable=broad-except
                # catch any unhandled exceptions and fail the ingest if the
                # client is already bound to help find critical bugs
                # and handle them consciously
                if next_task:
                    ingest_db = copy.copy(self.db)
                    ingest_db.bind(next_task.ingest_id)
                    ingest_db.fail()
                raise

        log.debug(f"{self.name} worker process exited gracefully")

    def wait_for_db(self):
        """Wait for database connection"""
        while not self.shutdown.is_set():
            if self.db.check_connection():
                break
            time.sleep(self.config.sleep_time)

    def graceful_shutdown_handler(self, signum, *_):
        """
        Set the shutdown event to not start any new tasks and give 15 seconds for the
        current task to finish. After 15s the task is failed using an alarm signal.
        """
        log.debug(f"{self.name} received {signum}, trying to shut down gracefully...")
        # next time shutdown will be forced
        signal.signal(signal.SIGINT, self.forced_shutdown_handler)
        signal.signal(signal.SIGTERM, self.forced_shutdown_handler)
        self.shutdown.set()
        signal.alarm(self.config.termination_grace_period)

    def forced_shutdown_handler(self, signum, *_):
        """
        Immediately raise an exception to hard shutdown the worker.
        This handler fires for example when the user double press CTRL+c.
        """
        log.debug(f"{self.name} received {signum} forced shutdown")
        raise errors.WorkerForcedShutdown


def alarm_handler(signum, frame):
    """
    Custom alarm signal handler that raises a timeout exception to indicate that
    the worker couldn't terminate gracefully in the given amount of time
    """
    raise errors.WorkerShutdownTimeout
