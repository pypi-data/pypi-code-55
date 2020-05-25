from threading import Thread
import json
import time
import logging
import grpc
from zeebe_grpc import gateway_pb2 as zeebe


class ZeebeWorker:

    def __init__(self, stub, worker_name, timeout=5 * 60 * 1000, request_timeout=1 * 60 * 1000,
                 max_jobs_to_activate=1, backoff_interval=5 * 1000):
        """Initiate a worker class with a stub, worker_name and some defaults
        """
        self.stub = stub
        self.worker_name = worker_name
        self.timeout = timeout
        self.request_timeout = request_timeout
        self.max_jobs_to_activate = max_jobs_to_activate
        self.backoff_interval = backoff_interval
        self.threads = {}

    def subscribe(self, task_type, target, timeout=None, request_timeout=None,
            max_jobs_to_activate=None, autocomplete=False, backoff_interval=None):
        """Subscribe to a task_type in a separate thread.
        Sets defaults based on class instance defaults.
        Runs _subscribe in a thread using the callable target or converts the target string to a
        method of self.
        """
        timeout = timeout or self.timeout
        request_timeout = request_timeout or self.request_timeout
        max_jobs_to_activate = max_jobs_to_activate or self.max_jobs_to_activate
        backoff_interval = backoff_interval or self.backoff_interval

        if not callable(target):
            target = getattr(self, target)

        thread = Thread(target=self._subscribe,
            args=[task_type, target, autocomplete],
            kwargs={
                'timeout': timeout,
                'request_timeout': request_timeout,
                'max_jobs_to_activate': max_jobs_to_activate,
                'backoff_interval': backoff_interval})
        thread.start()
        self.threads[task_type] = thread

    def _subscribe(self, task_type, target, autocomplete, timeout, request_timeout,
            max_jobs_to_activate, backoff_interval):
        """Handle communication with Zeebe
        It sends an ActivateJobsRequest with given params.
        When a job is received, it handles the job with target func.
        It catches any unhandled exception (through BaseException) and sends a FailJobRequest with
        the exception when this happens.
        """
        while True:
            logging.debug(f'Polling for {task_type}')
            try:
                req = zeebe.ActivateJobsRequest(
                    type=task_type,
                    worker=self.worker_name,
                    timeout=timeout,
                    requestTimeout=request_timeout,
                    maxJobsToActivate=max_jobs_to_activate)
                # ActivateJobsResponse returns as a stream, therefore a loop is used
                for resp in self.stub.ActivateJobs(req):
                    for job in resp.jobs:
                        logging.info(f'Handling job: {job.key} in instance:\
                                {job.workflowInstanceKey}')
                        try:
                            resp_variables = target(job)
                            if not isinstance(resp_variables, dict):
                                resp_variables = {}
                            if autocomplete:
                                complete_job_req = zeebe.CompleteJobRequest(
                                    jobKey=job.key, variables=json.dumps(resp_variables))
                                self.stub.CompleteJob(complete_job_req)
                                logging.info(f'Job handled: {job.key} in instance:\
                                        {job.workflowInstanceKey}')
                        # Catches every exception (https://docs.python.org/3.6/library/exceptions.
                        # html#exception-hierarchy)
                        except BaseException as e:
                            logging.error(repr(e), exc_info=True)
                            fail_job_req = zeebe.FailJobRequest(
                                jobKey=job.key, errorMessage=repr(e))
                            self.stub.FailJob(fail_job_req)
                            logging.info(f'Job failed: {job.key} in instance:\
                                    {job.workflowInstanceKey}')
            except grpc.RpcError as e:
                # All gRPC errors are caught, some need a backoff, some don't.
                # gRPC Statuscode dcos: https://github.com/grpc/grpc/blob/master/doc/statuscodes.md
                # Zeebe error docs: https://docs.zeebe.io/reference/grpc.html#error-handling

                # Handling errors with a backoff
                if e.code() == grpc.StatusCode.UNAVAILABLE:
                    logging.error('Cannot connect to Zeebe, retrying with backoff\n' + repr(e))
                    time.sleep(backoff_interval / 1000)
                elif e.code() == grpc.StatusCode.RESOURCE_EXHAUSTED:
                    logging.error(
                        'Zeebe cannot handle this amount of requests, retrying with a backoff\n'
                        + repr(e))
                    time.sleep(backoff_interval / 1000)
                elif e.code() == grpc.SatusCode.INTERNAL:
                    logging.error('Zeebe had an internal error between the gateway and the broker \
                                   Retrying with a backoff\n' + repr(e))
                    time.sleep(backoff_interval / 1000)
                # Silently handle all other errors and reconnect immediately
                elif e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                    logging.debug(f'No jobs for {task_type} found\n' + repr(e))
                elif e.code() == grpc.StatusCode.CANCELLED:
                    logging.debug(f'Request for {task_type} cancelled\n' + repr(e))
                else:
                    logging.debug(repr(e))
