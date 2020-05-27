import re
import os
import requests
import json
import numbers

import glog as log
import pandas as pd

from io import BytesIO, BufferedReader
from time import sleep
from zipfile import ZipFile

from .exceptions import NotEnoughFunds


class AppenAPI:
    """An abstract class for all Appen APIs.

    Attributes:
        _api_key (str): The API key that this API is using.
        _params (tuple): Default params for any Appen API requests.
        _base_endpoint (str): The base endpoint for all Appen APIs.

    """

    def __init__(self, api_key):
        """Create an AppenAPI.

        Args:
            api_key (str): Your Appen API key.

        """
        log.debug("Creating AppenAPI")
        assert(isinstance(api_key, str))
        self._api_key = api_key
        self._params = (
            ("key", self._api_key),
        )
        self._base_endpoint = "https://api.appen.com/v1/jobs"

    def _check_success(self, resp, error_message=None, success=200):
        """Check if the response from an Appen request was successful.

        Args:
            resp (requests.Response): The response object from a requests
                                      request.
            error_message (str, optional): A description of the error, if the
                                           request failed. Default: ""
            success (int, optional): The anticipated success code. Default: 200

        Raises:
            requests.exceptions.HTTPError: If `resp.status_code` is not equal
                                           to `success`

        """
        if error_message is None:
            error_message = ""

        if not isinstance(error_message, str):
            error_message = str(error_message)

        if not error_message.endswith(" "):
            error_message += " "

        error_message += f"Status Code: {resp.status_code}"

        if resp.status_code != success:
            log.error(f"{error_message}\n\n{resp.content}")
            raise requests.exceptions.HTTPError(error_message)


class AppenJob(AppenAPI):
    """A representation of an Appen Job."""

    def __init__(self, api_key, job_id):
        """Initialize an AppenJob object.

        Args:
            api_key (str): Your Appen API key.
            job_id (str, int): The Appen Job's ID.

        """
        super().__init__(api_key)
        self._job_id = job_id
        self._appen_json = None

    @property
    def appen_json(self):
        """Get Appen's Representation of the job.

        Returns:
            dict: Appen's Representation of the job.

        """
        if self._appen_json is None:
            resp = requests.get(f"{self._base_endpoint}/{self._job_id}.json",
                                params=self._params)
            self._check_success(resp, f"Failed to get job {self._job_id}.")
            self._appen_json = resp.json()

        return self._appen_json

    def _update_parameter_data(self, data, *parameters):
        """Update most parts of the Appen Job json.

        Args:
            data (str): The new value to update to in the Appen json.
            *parameters (str): The field in the Appen json to update.
                               Multiple fields implies depth in the json.

        Reference:
            https://success.appen.com/hc/en-us/articles/202703425-Appen-API-Requests-Guide

        """
        assert(all(isinstance(parameter, str) for parameter in parameters))

        try:
            data = str(data)
        except Exception:
            raise ValueError(f"Unable to cast {type(data)} to {type(str)}")

        endpoint = f"{self._base_endpoint}/{self._job_id}.json"

        data_params = "".join([f"[{p}]" for p in parameters])
        params = (
            *self._params,
        )
        data = {
            f"job{data_params}": data
        }
        resp = requests.put(endpoint, params=params, data=data)
        self._check_success(resp, (f"Failed to update {parameters}"
                                   f" for job {self._job_id}."))

    class __reset_appen_job_json:
        def __init__(self, f):
            self.f = f

        def __call__(self, inst, *args, **kwargs):
            inst._appen_json = None
            return self.f(inst, *args, **kwargs)

    @property
    def title(self):
        """str: The title of the job."""
        return self.appen_json["title"]

    @title.setter
    @__reset_appen_job_json
    def title(self, title):
        self._update_parameter_data(title, "title")

    @property
    def instructions(self):
        """str: The instructions html of the job."""
        return self.appen_json["instructions"]

    @instructions.setter
    @__reset_appen_job_json
    def instructions(self, instructions):
        assert(isinstance(instructions, str))
        self._update_parameter_data(instructions, "instructions")

    @property
    def cml(self):
        """str: The Custom Markup Language task template for the job."""
        return self.appen_json["cml"]

    @cml.setter
    @__reset_appen_job_json
    def cml(self, cml):
        assert(isinstance(cml, str))
        self._update_parameter_data(cml, "cml")

    @property
    def payment_cents(self):
        """float: The amount paid to annotators per unit/row completed."""
        return self.appen_json["payment_cents"]

    @payment_cents.setter
    @__reset_appen_job_json
    def payment_cents(self, payment_cents):
        assert(isinstance(payment_cents, numbers.Number))
        self._update_parameter_data(str(payment_cents), "payment_cents")

    @property
    def judgments_per_unit(self):
        """int: The number of annotatorions required, per unit/row."""
        return self.appen_json["judgments_per_unit"]

    @judgments_per_unit.setter
    @__reset_appen_job_json
    def judgments_per_unit(self, judgments_per_unit):
        assert(isinstance(judgments_per_unit, numbers.Number))
        self._update_parameter_data(judgments_per_unit, "judgments_per_unit")

    @property
    def req_ttl_in_seconds(self):
        """float: The number of seconds per page/assignment."""
        return self.appen_json["options"]["req_ttl_in_seconds"]

    @req_ttl_in_seconds.setter
    @__reset_appen_job_json
    def req_ttl_in_seconds(self, req_ttl_in_seconds):
        assert(isinstance(req_ttl_in_seconds, numbers.Number))
        self._update_parameter_data(req_ttl_in_seconds,
                                    "options",
                                    "req_ttl_in_seconds")

    @property
    def units_per_assignment(self):
        """int: The number of units/rows per page/assignment."""
        return self.appen_json["units_per_assignment"]

    @units_per_assignment.setter
    @__reset_appen_job_json
    def units_per_assignment(self, units_per_assignment):
        assert(isinstance(units_per_assignment, numbers.Number))
        self._update_parameter_data(units_per_assignment,
                                    "units_per_assignment")

    @property
    def auto_launch(self):
        """bool: Whether auto-launch is enabled."""
        return self.appen_json["auto_order"]

    @auto_launch.setter
    @__reset_appen_job_json
    def auto_launch(self, auto_launch):
        assert(isinstance(auto_launch, numbers.Number))
        self._update_parameter_data(auto_launch, "auto_order")

    @property
    def reject_at(self):
        """int: Minimum annotator accuracy."""
        return self.appen_json["options"]["reject_at"]

    @reject_at.setter
    @__reset_appen_job_json
    def reject_at(self, reject_at):
        assert(isinstance(reject_at, numbers.Number))
        self._update_parameter_data(reject_at, "options", "reject_at")

    @property
    def id(self):
        """int: The job id."""
        return self._job_id

    @property
    def status(self):
        """dict: The number of units/rows by whether they've been completed or not.

        To Do:
            Add logic and return a string (i.e. In Progess, Complete, etc.)
        """
        endpoint = f"{self._base_endpoint}/{self.id}/ping.json"

        resp = requests.get(endpoint, params=self._params)
        self._check_success(resp)

        return resp.json()

    def upload_csv(self, csv, convert_test_questions=False, match_cml=False):
        """Upload units/rows to Appen job.

        Args:
            csv (str, pandas.Dataframe): A local path or a remote url to a csv,
                                         or a pandas.DataFrame.
            convert_test_questions (bool, optional): Converts all rows with
                                                     the `_golden` column set
                                                     to True if True.
                                                     Default: False
            match_cml (bool, optional): When converting test questions,
                                        Appen may add the `gold=True`
                                        attribute to the job's CML. If you wish
                                        to prevent Appen from doing,
                                        this set `match_cml` to `True`. Only
                                        works when `convert_test_questions` is
                                        `True`. Default: False

        """
        name = "sample.csv"
        if isinstance(csv, str) and os.path.exists(csv):
            name = csv
            csv = pd.read_csv(csv)

        assert(isinstance(csv, pd.DataFrame))
        endpoint = f"{self._base_endpoint}/{self.id}/upload.json"
        headers = {
            "Content-Type": "text/csv"
        }

        params = (
            *self._params,
            ("force", True)
        )

        filelike = BytesIO(csv.to_csv(index=False).encode())
        filelike.name = name
        resp = requests.put(endpoint,
                            headers=headers,
                            params=params,
                            data=BufferedReader(filelike))

        self._check_success(resp)

        if match_cml:
            cml = self.cml

        if convert_test_questions:
            for _ in range(100):
                if self.status["all_units"] >= csv.shape[0]:
                    break
                sleep(1)
            endpoint = f"{self._base_endpoint}/{self.id}/gold.json"
            resp = requests.put(endpoint, params=self._params)
            self._check_success(resp)

        if match_cml:
            for _ in range(100):
                if cml != self.cml:
                    break
                sleep(1)
            self.cml = cml

    def pause(self):
        """Pause the Appen job."""
        endpoint = f"{self._base_endpoint}/{self.id}/pause.json"

        resp = requests.get(endpoint, params=self._params)
        self._check_success(resp, f"Failed to pause job {self.id}")

    def resume(self):
        """Resume the Appen job."""
        endpoint = f"{self._base_endpoint}/{self.id}/resume.json"

        resp = requests.get(endpoint, params=self._params)
        self._check_success(resp, f"Failed to resume job {self.id}")

    def cancel(self):
        """Cancel the Appen job."""
        endpoint = f"{self._base_endpoint}/{self.id}/cancel.json"

        resp = requests.get(endpoint, params=self._params)
        self._check_success(resp, f"Failed to cancel job {self.id}")

    def launch(self, on_demand=False, internal=False, n_units=None):
        """Launch the job to your internal and/or the on-demand workforces.

        Args:
            on_demand (bool, optional): Have the on-demand workforce process
                                        `n_units` of rows/units.
            internal (bool, optional): Have the internal workforce process
                                       `n_units` of rows/units.
            n_units (int, optional): The number of rows/units to launch. If
                                     None, all units will be launched.

        """
        if n_units is None:
            status = self.status
            n_units = status["all_units"]
            n_units -= status["golden_units"]
            n_units -= status["ordered_units"]

        n_units = int(n_units)

        if not on_demand and not internal:
            log.warning(
                f"Attempting to launch job {self.id} with no annotators.")

        if not n_units > 0:
            log.warning(
                f"Unable to launch job {self.id} because"
                f" {n_units} units were requested.")

        endpoint = f"{self._base_endpoint}/{self.id}/orders.json"
        n_channels = 0
        data = {"debit[units_count]": n_units}

        if on_demand:
            data.update({f"channels[{n_channels}]": "on_demand"})
            n_channels += 1

        if internal:
            data.update({f"channels[{n_channels}]": "cf_internal"})
            n_channels += 1

        resp = requests.post(endpoint, params=self._params, data=data)
        resp_content = resp.content.decode()
        out_of_funds_match = re.match(
            (".*Your team has \$(?P<has>\d+\.\d+),"
             " but this launch will cost \$(?P<needs>\d+\.\d+).*"),
            resp_content)

        if out_of_funds_match:
            funds = out_of_funds_match.groupdict()
            raise NotEnoughFunds(
                f"Your team has ${funds['has']}, "
                f"but this launch will cost ${funds['needs']}"
            )
        self._check_success(resp)

    def _get_report(self, report_type):
        endpoint = f"{self._base_endpoint}/{self.id}.csv"
        params = (
            *self._params,
            ("type", report_type)
        )

        resp = requests.get(endpoint, params)
        while resp.status_code == 202:
            sleep(60)
            resp = requests.get(endpoint, params)

        self._check_success(resp)

        csv_zip = ZipFile(BytesIO(resp.content))
        csv_filelike = BytesIO(csv_zip.read(csv_zip.filelist[0].filename))
        csv = pd.read_csv(csv_filelike)
        return csv

    def get_report(self, aggregated=False, full=False):
        """Download the latest Appen report(s) for this job.

        Args:
            aggregated (bool, optional): Download the Appen Aggregated
                                         report for this job.
            full (bool, optional): Download the Appen Full report for
                                   this job.

        Returns:
            pandas.DataFrame, optional: The Aggregated report. Only provided if
                                        `aggregated` is True.
            pandas.DataFrame, optional: The Full report. Only provided if
                                        `full` is True.

        """
        reports = []
        if aggregated:
            reports.append(self._get_report("aggregated"))

        if full:
            reports.append(self._get_report("full"))

        if len(reports) > 1:
            return tuple(reports)
        else:
            return reports[0]

    def add_tags(self, *tags):
        """Add tags to the Appen job.

        Args:
            *tags (str): Tags to add to the Appen job.

        """
        endpoint = f"{self._base_endpoint}/{self.id}/tags"
        data = {"tags": ",".join(tags)}
        resp = requests.post(endpoint, params=self._params, data=data)
        self._check_success(resp)

    def delete_tags(self, *tags):
        """Remove tags from the Appen job.

        Args:
            *tags (str): Tags to remove from the Appen job.

        """
        endpoint = f"{self._base_endpoint}/{self.id}/tags"
        data = {"tags": ",".join(tags)}
        resp = requests.delete(endpoint, params=self._params, data=data)
        self._check_success(resp)


class AppenClient(AppenAPI):
    """A client for interacting with Appen.

    Currently, it only creates, copies, and deletes jobs.

    """

    def __init__(self, api_key):
        """Initialize an AppenClient.

        Args:
            api_key (str): Your Appen API key.

        """
        super().__init__(api_key)

    def create_job(self, title, instructions, cml):
        """Create a brand new Appen job.

        Args:
            title (str): The title of this job.
            instructions (str): The instructions html for this job.
            cml (str): The Custom Markup Language task template for this job.

        Returns:
            AppenJob: A AppenJob object.

        """
        endpoint = f"{self._base_endpoint}.json"
        added_params = (
            ("job[title]", title),
            ("job[instructions]", instructions),
            ("job[cml]", cml))

        resp = requests.post(
            endpoint,
            data=dict(added_params),
            params=self._params)

        job_id = resp.json()["id"]

        return AppenJob(self._api_key, job_id)

    def copy_job(self, job_id, units=None):
        """Copy another Appen job.

        Args:
            job_id (str, int): The id of the job to copy from.
            units (str, optional): Which rows/units to copy.
                                   Options: 'all', 'gold', None.
                                   Default: None

        Raises:
            AssertionError: if `units` is not 'all', 'gold', or None

        Returns:
            AppenJob: A AppenJob object.

        To Do:
            1. Replace `units` with `gold` and `not_gold` booleans
            2. Rename `job_id` to `job` and allow `job` to be an AppenJob

        """
        assert(units is None or units == "gold" or units == "all")
        endpoint = f"{self._base_endpoint}/{job_id}/copy.json"

        params = self._params
        if units == "gold":
            params = (*params, ("gold", True))

        if units == "all":
            params = (*params, ("all_units", True))

        resp = requests.get(endpoint, params=params)
        self._check_success(resp, f"Unable to copy job from {job_id}")

        return AppenJob(self._api_key, resp.json()["id"])

    def delete_job(self, job_id):
        """Delete an Appen Job.

        Args:
            job_id (str, int): The id of the job to delete.

        Returns:
            requests.Response: The response from Appen.

        To Do:
            1. Rename `job_id` to `job` and allow `job` to be an AppenJob
            2. Auto-check deletion success. Appen returns 200 codes,
               even on failures.

        """
        endpoint = f"https://api.appen.com/v1/jobs/{job_id}.json"

        resp = requests.delete(endpoint, params=self._params)
        # self._check_success(resp, f"Unable to delete job {job_id}")
        return resp

    def iter_jobs(self, team_id=None):
        """Iterate through current F8 jobs.

        Args:
            team_id (str, int): An id for the team's jobs to iterate through

        Yields:
            AppenJob: A Appen job that owned by the team

        """
        endpoint = f"{self._base_endpoint}.json"

        page = 1
        while True:
            params = (*self._params, ("page", page))
            resp = requests.get(endpoint, params=params)
            self._check_success(resp, "Failed to find any jobs")

            jobs = json.loads(resp.content.decode())
            if len(jobs) == 0:
                break

            for job in jobs:
                yield AppenJob(self._api_key, job["id"])

            if len(jobs) < 10:
                break
