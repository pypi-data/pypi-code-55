"""
All client requests.
"""

# pylint: disable=C0111 # (no docstrings)

import time
import requests
from colors import color
from .version import __version__

DEFAULT_SERVER = "http://localhost:3005"
DEFAULT_POLL_INTERVAL = 3000.0  # [ms]
LOG_SEPARATOR = "====================================================================="
LOG_MORE_HINT = "Please refer to the job results and previous logs for more details."
SKIP_EXCEPTION_FOR_ERRORS = ["DOWNLOAD_PARTIALLY_FAILED"]


class TeroDataClient:
    def __init__(
        self,
        username,
        server=DEFAULT_SERVER,
        log=True,
        color_logs=True,
        poll_interval=DEFAULT_POLL_INTERVAL,
    ):
        self.username = username
        self.base_url = "%s/api" % server
        self.log_enabled = log
        self.color = color if color_logs else color_bypass
        self.poll_interval = poll_interval

    def get_datasets(self):
        url = "%s/datasets" % self.base_url
        return self._get(url)

    def get_dataset(self, dataset_id):
        url = "%s/dataset/%s" % (self.base_url, dataset_id)
        return self._get(url)

    # ====================================
    def create_query_job(self, dataset_id, attrs, process_response_errors=True):
        url = "%s/dataset/%s/query" % (self.base_url, dataset_id)
        return self._post(url, attrs, process_response_errors)

    def query(self, dataset_id, attrs, on_progress=None):
        job = None
        previous_logs = {}
        colorize = lambda msg: self.color(msg, fg="cyan")
        try:
            # Create job
            job = self.create_query_job(
                dataset_id, attrs, process_response_errors=False
            )
            self._log_job_id(job)
            self._maybe_raise_api_exception(job)

            # Poll job status until it finishes
            while not is_job_finished(job):
                time.sleep(self.poll_interval / 1e3)
                job = self.get_job(job["id"], process_response_errors=False)
                if self.log_enabled:
                    self._log_query_status(previous_logs, job)
                if on_progress:
                    on_progress(job)
                self._maybe_raise_api_exception(job)

            return job
        finally:
            # Cancel job if it's still running
            # (user may have hit CTRL-C, and the server needs to know!!)
            self.cancel_job_if_running(job)

            # Irrespective of the job's outcome, show logs
            if self.log_enabled and job and "id" in job:
                normalize_job_for_logging(job, "query")
                log_clear()
                if len(job["granuleIds"]):
                    print("Found granule IDs:")
                    for granule_name in job["granuleIds"]:
                        print(f"- {granule_name}")
                print("")
                print(colorize(LOG_SEPARATOR))
                print(colorize("JOB SUMMARY"))
                print(colorize(f"Job {job['id']} {job['status']} ({job['progress']}%)"))
                print(
                    colorize(
                        "Found granules: %d. Estimated size: %.1f MB"
                        % (job["numGranules"], job["totalSize"])
                    )
                )
                print(colorize(LOG_MORE_HINT))
                print(colorize(LOG_SEPARATOR))
            if self.log_enabled and job and not "id" in job and "_errorCode" in job:
                log_clear()
                print(colorize(LOG_SEPARATOR))
                print(colorize("JOB SUMMARY"))
                print(colorize(f"Job is errored with code {job['_errorCode']}"))
                print(colorize(job["_errorDescription"]))
                print(colorize(LOG_SEPARATOR))

    # ====================================
    def create_download_job(
        self,
        dataset_id,
        granule_ids,
        max_size=None,
        output_path=None,
        process_response_errors=True,
    ):
        url = "%s/dataset/%s/download" % (self.base_url, dataset_id)
        spec = {
            "granuleIds": granule_ids,
            "maxSize": max_size,
            "outputPath": output_path,
        }
        return self._post(url, spec, process_response_errors=process_response_errors)

    def download(
        self, dataset_id, granule_ids, max_size=None, output_path=None, on_progress=None
    ):
        job = None
        previous_logs = {}
        colorize = lambda msg: self.color(msg, fg="cyan")
        try:
            # Create job
            job = self.create_download_job(
                dataset_id,
                granule_ids,
                max_size,
                output_path,
                process_response_errors=False,
            )
            self._log_job_id(job)
            self._maybe_raise_api_exception(job)

            # Poll job status until it finishes
            while not is_job_finished(job):
                time.sleep(self.poll_interval / 1e3)
                job = self.get_job(job["id"], process_response_errors=False)
                if self.log_enabled:
                    self._log_download_status(previous_logs, job)
                if on_progress:
                    on_progress(job)
                self._maybe_raise_api_exception(job)

            return job
        finally:
            # Cancel job if it's still running
            # (user may have hit CTRL-C, and the server needs to know!!)
            self.cancel_job_if_running(job)

            # Irrespective of the job's outcome, show logs
            if self.log_enabled and job:
                normalize_job_for_logging(job, "download")
                log_clear()
                print("")
                print(colorize(LOG_SEPARATOR))
                print(colorize("JOB SUMMARY"))
                print(colorize(f"Job {job['id']} {job['status']} ({job['progress']}%)"))
                print(
                    colorize(
                        "Requested granules: %d. Downloaded: %d (%.1f MB). Errored: %d"
                        % (
                            len(job["granuleIds"]),
                            job["numDownloaded"],
                            job["totalDownloadSize"],
                            len(job["erroredGranules"]),
                        )
                    )
                )
                print(colorize(LOG_MORE_HINT))
                print(colorize(LOG_SEPARATOR))

    # ====================================
    def get_jobs(self):
        url = "%s/jobs" % (self.base_url)
        return self._get(url)

    def get_job(self, job_id, process_response_errors=True):
        url = "%s/job/%s" % (self.base_url, job_id)
        return self._get(url, process_response_errors=process_response_errors)

    def cancel_job(self, job_id):
        url = "%s/job/%s" % (self.base_url, job_id)
        return self._delete(url)

    # ====================================
    # Generic helpers
    # ====================================
    def cancel_job_if_running(self, job):
        if (job is None) or not "id" in job or is_job_finished(job):
            return
        self.cancel_job(job["id"])
        job["status"] = "CANCELED"

    # ====================================
    # I/O helpers
    # ====================================
    def _get(self, url, process_response_errors=True):
        return self._request(url, process_response_errors=process_response_errors)

    def _post(self, url, json, process_response_errors=True):
        return self._request(
            url,
            method="post",
            json=json,
            process_response_errors=process_response_errors,
        )

    def _delete(self, url, process_response_errors=True):
        return self._request(
            url, method="delete", process_response_errors=process_response_errors
        )

    def _request(self, url, method="get", json=None, process_response_errors=True):
        headers = {"x-tero-client": f"tero-data-client-python@{__version__}"}
        username = self.username if self.username is not None else ""
        if method == "get":
            res = requests.get(url, auth=(username, ""), headers=headers)
        elif method == "post":
            res = requests.post(url, auth=(username, ""), headers=headers, json=json)
        elif method == "delete":
            res = requests.delete(url, auth=(username, ""), headers=headers)
        if res.headers.get("content-type").startswith("application/json"):
            out = res.json()
            if process_response_errors:
                self._maybe_raise_api_exception(out)
            return out
        res.raise_for_status()
        return None

    # ====================================
    # Exceptions
    # ====================================
    def _maybe_raise_api_exception(self, job):
        if job is None:
            return
        if "_errorCode" in job:
            if self.log_enabled:
                log_clear()
            msg = "%s %s: %s" % (
                job["_errorHttpStatusCode"],
                job["_errorCode"],
                job["_errorDescription"],
            )
            if job["_errorCode"] in SKIP_EXCEPTION_FOR_ERRORS:
                print(self.color(msg, fg="red"))
            else:
                raise Exception(msg)

    def _raise_custom_exception(self, http_status_code, code, description):
        if self.log_enabled:
            print("")
        raise Exception("%s %s: %s" % (http_status_code, code, description))

    # ====================================
    # Logs
    # ====================================
    def _log_job_id(self, job):
        if not self.log_enabled or not "id" in job:
            return
        print(
            f"Job {self.color(job['id'], fg='cyan', style='bold')} created. "
            + "Keep this ID handy for future reference."
        )

    def _log_query_status(self, previous_logs, job):
        job_type = "query"
        normalize_job_for_logging(job, job_type)
        self._log_notes(previous_logs, job)
        self._log_status(job, job_type)  # final one, since it doesn't add newline

    def _log_download_status(self, previous_logs, job):
        job_type = "download"
        normalize_job_for_logging(job, job_type)

        # Log download results
        for id in list(job["granulePaths"]):
            msg = f"{self.color('* Downloaded', fg='green')} {id}"
            log_message(previous_logs, msg)
        for id in list(job["erroredGranules"]):
            err = job["erroredGranules"][id]
            msg = "%s %s: %s %s" % (
                self.color("* ERROR downloading", fg="red"),
                id,
                self.color(
                    f'{err["_errorHttpStatusCode"]} {err["_errorCode"]}', fg="red",
                ),
                err["_errorDescription"],
            )
            log_message(previous_logs, msg)

        # Basic logs
        self._log_notes(previous_logs, job)
        self._log_status(job, job_type)  # final one, since it doesn't add newline

    def _log_notes(self, previous_logs, job):
        for note in job["_notes"]:
            msg = self.color(
                f"{LOG_SEPARATOR}\nNote from the server for job {job['id']}:\n--> {note}\n{LOG_SEPARATOR}",
                fg="yellow",
            )
            log_message(previous_logs, msg)

    def _log_status(self, job, job_type):
        msg = "%s %s job %s: %s%%  " % (
            job["status"],
            job_type,
            job["id"],
            job["progress"],
        )
        print(self.color(msg, fg="yellow"), end="\r", flush=True)


# ====================================
# Helpers
# ====================================
# Sometimes jobs come with just an error.
# Ensure typical fields needed for logging are present
def normalize_job_for_logging(job, job_type=None):
    if not "id" in job:
        job["id"] = "_unknown_id_"
    if not "status" in job:
        job["status"] = "_unknown_status_"
    if not "progress" in job:
        job["progress"] = "?"
    if not "_notes" in job:
        job["_notes"] = []
    if job_type == "download":
        if not "granuleIds" in job:
            job["granuleIds"] = []
        if not "numDownloaded" in job:
            job["numDownloaded"] = 0
        if not "totalDownloadSize" in job:
            job["totalDownloadSize"] = 0
        if not "granulePaths" in job:
            job["granulePaths"] = {}
        if not "erroredGranules" in job:
            job["erroredGranules"] = {}


def is_job_finished(job):
    return job["status"] in ["FINISHED", "CANCELED", "ERRORED"]


def log_clear():
    print(" " * 70, end="\r", flush=True)


def log_message(previous_logs, msg):
    if msg in previous_logs:
        return
    log_clear()
    previous_logs[msg] = True
    print(msg)


def color_bypass(msg, **kwargs):
    return msg
