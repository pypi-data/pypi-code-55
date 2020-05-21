import asyncio
import collections
import logging
import random
import time
from functools import wraps

from qiskit.providers import BaseJob, JobError, JobStatus
from qiskit.result import Result

from qctic.utils import wait_result, wait_result_async

_PARAM_TIMEOUT = "timeout"
_PARAM_WAIT = "wait"

_logger = logging.getLogger(__name__)


def _fetch_job_sync(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        fetch = kwargs.pop("fetch", False)

        if not args[0]._remote_job or fetch:
            args[0].fetch_remote()

        return func(*args, **kwargs)

    return wrapper


def _fetch_job_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        fetch = kwargs.pop("fetch", False)

        if not args[0]._remote_job or fetch:
            await args[0].fetch_remote_async()

        return await func(*args, **kwargs)

    return wrapper


async def _dummy_submit_task():
    _logger.debug((
        "Waiting on dummy submit task: "
        "Was job.submit() in backend.run() synchronous?"
    ))


WaitResultParams = collections.namedtuple(
    "WaitResultParams",
    ["timeout", "wait"])


class QCticJob(BaseJob):
    """A Qiskit job that is executed remotely in the CTIC Erwin simulation platform."""

    def __init__(self, backend, job_id, qobj, run_params=None, remote_job=None):
        """Constructor.

        Args:
            backend (QCticQasmSimulator): Backend that contains this job.
            job_id (str): ID of the job.
            qobj (Qobj): Qobj that contains the experiment.
            run_params (dict): Optional dict of arbitrary arguments passed
                to the ``run`` method in the remote simulation platform.
        """

        super().__init__(backend, job_id)
        self._qobj = qobj
        self._remote_job = remote_job
        self._fetch_time = None
        self._run_params = run_params
        self._submit_task = None

    @property
    def api(self):
        """QCticAPI: The API instance of this job's backend."""

        return self.backend().api

    def qobj(self):
        """Return the Qobj submitted for this job.

        Returns:
            Qobj: The Qobj submitted for this job.
        """

        return self._qobj

    @property
    def run_params(self):
        """dict: Arguments passed to the ``run`` method in the remote simulation platform."""

        return self._run_params

    @property
    def remote_job(self):
        """dict: Serialized version of this job as represented in the remote API."""

        return self._remote_job

    @property
    def submit_task(self):
        return self._submit_task if self._submit_task else _dummy_submit_task()

    @submit_task.setter
    def submit_task(self, val):
        if self._submit_task:
            raise ValueError("The submit task has already been defined")

        self._submit_task = val

    def _log_fetch(self):
        _logger.debug("Fetching job: %s", self.job_id())

    def fetch_remote(self):
        self._log_fetch()
        self._remote_job = self.api.get_job_sync(self.job_id())
        self._fetch_time = time.time()

    async def fetch_remote_async(self):
        self._log_fetch()
        self._remote_job = await self.api.get_job(self.job_id())
        self._fetch_time = time.time()

    def _result(self):
        error = self._remote_job.get("error", None)

        if error is not None:
            raise JobError(error)

        result_dict = self._remote_job.get("result", None)

        return Result.from_dict(result_dict) if result_dict else None

    def _status(self):
        return self._remote_job.get("status", None)

    def _get_wait_params(self, *args, **kwargs):
        if _PARAM_TIMEOUT not in kwargs or _PARAM_WAIT not in kwargs:
            return None

        wait = int(kwargs[_PARAM_WAIT])
        timeout = kwargs[_PARAM_TIMEOUT]

        if timeout is not None:
            timeout = int(timeout)

        _logger.debug(
            "Should wait for result (timeout=%s, wait=%s)",
            timeout, wait)

        return WaitResultParams(timeout=timeout, wait=wait)

    @_fetch_job_sync
    def status(self):
        """Return the status of the job, one of the names of the ``JobStatus`` enum.

        Args:
            fetch (bool): (Optional) Fetch the status from the remote API.

        Returns:
            JobStatus: The name of a member of the JobStatus enum.
        """

        return self._status()

    def submit(self):
        """Submit the job to the backend for execution."""

        self.api.post_job_sync(self)

    def cancel(self):
        """Attempt to cancel the job."""

        self.api.cancel_job_sync(self.job_id())

    @_fetch_job_sync
    def result(self, *args, **kwargs):
        """Return the results of the job.

        Args:
            fetch (bool): (Optional) Fetch the result from the remote API.

        Returns:
            Result: The results.

        Raises:
            JobError: If there was an error running the experiment on the remote simulator.
        """

        wait_params = self._get_wait_params(*args, **kwargs)

        if wait_params:
            return wait_result(
                self,
                base_sleep=wait_params.wait,
                timeout=wait_params.timeout,
                sleep_growth=1.0)

        return self._result()

    @_fetch_job_async
    async def status_async(self):
        return self._status()

    async def submit_async(self):
        await self.api.post_job(self)

    async def cancel_async(self):
        await self.api.cancel_job(self.job_id())

    @_fetch_job_async
    async def result_async(self, *args, **kwargs):
        wait_params = self._get_wait_params(*args, **kwargs)

        if wait_params:
            return await wait_result_async(
                self,
                base_sleep=wait_params.wait,
                timeout=wait_params.timeout,
                sleep_growth=1.0)

        return self._result()
