"""Data structures to handle BigBlueButton servers

This module also contains group handling support and the implementation
of the communication with the API itself. Meetings and attendees manage
themselves by talking to the BigBlueButton object linked to them. All
other methods should be called on a BigBlueButtonGroup, which takes care
of routing to the appropriate server(s).
"""

import concurrent.futures
import json
import logging
import random
import subprocess  # noqa: S404
from dataclasses import dataclass, field
from hashlib import sha1
from socket import getfqdn
from typing import Any, Callable, Dict, Optional, Sequence, Tuple, Union
from urllib.parse import urlencode
from uuid import uuid1

import requests
import xmltodict

from .attendee import Attendee
from .loadbalancing import CHECKERS as lb_checkers
from .meeting import Meeting

try:
    from sadf import SadfCommand, SadfReport
    import sadf.fieldgroups as sadf_fieldgroups
except ImportError:
    SadfCommand, SadfReport, sadf_fieldgroups = None, None, None


logger = logging.getLogger(__name__)


@dataclass
class BigBlueButton:
    """One BigBlueButton server.

    A BigBlueButton instance holds the information needed to communicate with the
    BigBlueButton server. When creating meetings, it passes itself to the Meeting
    object, and provides methods for the Meeting object to manage itself.

    A BigBlueButton server always belongs to a BigBlueButtonGroup, which it gets
    passed in the constructor and it registers itself with.
    """

    group: "BigBlueButtonGroup"
    name: str

    url: str
    salt: str
    host: Optional[str] = None

    meetings: dict = field(default_factory=dict)
    sysstat: Optional[SadfReport] = None

    request_timeout: Union[int, float, Tuple[Union[int, float], Union[int, float]]] = (0.5, 10)

    def __post_init__(self):
        self.group.apis[self.name] = self
        logger.debug(f"Self-registered server {self.name} in group {self.group.name}")

        # Use persistent HTTP session to track JSESSIONID cookie (et al)
        self._session = requests.Session()

    @staticmethod
    def request_checksum(call: str, query: str, salt: str) -> str:
        """Compute the checksum needed to authenticate API requests to a BigBlueButton server.

        The checksum has to be sent with every API request and is constructed like this:

          1. Build the full query string (already done when passed into this method)
          2. Prepend the name of the API call, without delimiter
          3. Append the API salt (shared secret, key,…) provided by the BBB server
          4. Calculate the SHA1 sum of the resulting string

        >>> BigBlueButton.request_checksum("isMeetingRunning", "meetingID=Foo", "MyTestSalt")
        'f59b73c5cf1db387da4ca7d937049420d4c50a12'

        The resulting checksum is added tothe original query string as a parameter called
        checksum.
        """
        hash_string = call + query + salt
        checksum = sha1(hash_string.encode()).hexdigest()  # noqa: S303, we have no choice

        return checksum

    def _build_url(self, call: str, params: Optional[Dict[str, str]] = None) -> str:
        # Generate query string with challenge-response checksum
        # cf. https://docs.bigbluebutton.org/dev/api.html#usage
        query = urlencode(params or {})
        query += "&checksum=" + self.request_checksum(call, query, self.salt)

        url = f"{self.url}{call}?{query}"
        return url

    def _request(self, call: str, params: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        url = self._build_url(call, params)

        res = self._session.get(url, timeout=self.request_timeout)
        xml = xmltodict.parse(res.text)

        return xml["response"]

    def create_meeting(self, do_create=True, *args, **kwargs) -> Meeting:
        """Create a meeting on thie BigBlueButton server.

        args and kwargs are passed verbatim into the Meeting constructor.

        This method first looks up whether a meeting with the passed meeting_id
        and reuse that object if a meeting is found. If none is found, a new object
        is created and the create API call sent to the server (if do_create is not
        set to False).

        The BigBlueButton API guarantees that the create call is idempotent,
        so calling this method on a meeting ID of an existing meeting is safe. But,
        as every server is part of a server group, consumers should always call
        create_meeting on a BigBlueBUttonGroup instead. This method does NOT
        verify that the meeting is non-existent on other servers.
        """
        meeting_id = kwargs["meeting_id"]
        if meeting_id in self.meetings:
            meeting = self.meetings[meeting_id]
        else:
            meeting = Meeting(self, *args, **kwargs)

        if do_create:
            meeting.create()
        else:
            meeting.get_meeting_info()

        return meeting

    def get_meetings(self):
        """Get all meetings known on the BigBlueButtonServer.

        This method calls the getMeetings API call on the BigBlueButton server
        and constructs Meeting objects from all meetings in the result.

        As every server is part of a server group, consumers should always call
        create_meeting on a BigBlueBUttonGroup instead. This method does NOT
        verify that the meeting is non-existent on other servers.
        """
        logger.info(f"Updating meetings on server {self.name}")
        res = self._request("getMeetings")

        if "meetings" not in res or not res["meetings"] or not res["meetings"]["meeting"]:
            self.meetings.clear()
            logger.info(f"Cleared all meetings from server {self.name}")
        else:
            if not isinstance(res["meetings"]["meeting"], list):
                res["meetings"]["meeting"] = [res["meetings"]["meeting"]]

            for meeting_dict in res["meetings"]["meeting"]:
                meeting_id = meeting_dict["meetingID"]

                if meeting_id in self.meetings:
                    meeting = self.meetings[meeting_id]
                    logger.debug(f"Meeting {meeting_id} already known on server {self.name}")
                else:
                    meeting = Meeting(self, meeting_id=meeting_id)
                    self.meetings[meeting_id] = meeting
                    logger.debug(f"Meeting {meeting_id} discovered, adding to server {self.name}")

                meeting._update_from_response(meeting_dict)

        return self.meetings

    def ssh_command(
        self, command: Sequence[str], input_: Optional[str] = None
    ) -> subprocess.CompletedProcess:
        """Execute a shell command through an SSH connection to the server.

        This method constructs an ssh command and runs it as a subprocess,
        without shell expansion. However, shell expansion WILL take place
        on the server side.

        The subprocess result is returned verbatim.
        """
        args = ["ssh", self.host] + list(command)

        logger.info(f"Running SSH command {args} on {self.name}")
        res = subprocess.run(  # noqa: S603, command injection is intended
            args, capture_output=True, input=input_, text=True
        )
        return res

    def get_sysstat(self) -> SadfReport:
        """Get the output of the sadf/sar command (from the sysstat package) through SSH.

        The result is used when load-balancing API requests.

        To use this functaionality, the sadf Python package (in the "sysstat" extra)
        must be installed.
        """
        if SadfCommand is None:
            logger.warn(f"sysstat requested on host {self.name}, but python-sadf unavailable")
            self.sysstat = None
            return

        logger.info(f"Getting system statistics on server {self.name}")

        # Let the python-sadf library build a command, but do not run it
        sadf_cmd = SadfCommand()
        sadf_cmd.field_groups = [
            sadf_fieldgroups.CPULoad(all_fields=True),
            sadf_fieldgroups.IO(),
            sadf_fieldgroups.Kernel(),
            sadf_fieldgroups.Memory(all_fields=True),
            sadf_fieldgroups.Network(dev=True, edev=True, sock=True),
            sadf_fieldgroups.Queue(),
        ]
        cmd = sadf_cmd._build_command()
        # Prepend environment python-sadf woud use
        cmd = ["env"] + [f"{k}={v}" for k, v in sadf_cmd._command_env.items()] + cmd

        # Execute using our own runner and extract data
        ret = self.ssh_command(cmd)
        if ret.returncode == 0:
            try:
                host_data = json.loads(ret.stdout)["sysstat"]["hosts"][0]
            except (KeyError, json.JSONDecodeError):
                logger.error(f"sadf produced invalid data on host {self.name}")
            else:
                # Hand back to python-sadf to generate pandas report
                self.sysstat = SadfReport(host_data, sadf_cmd.field_groups)
        else:
            logger.warn(f"sadf unavailable or failing on host {self.name}")

        return self.sysstat

    def refresh(self):
        """Refresh various aspects of this server.

          - Meetings
          - Sysstat data
        """
        logger.debug(f"Fully refreshing server {self.name}")
        self.get_meetings()
        self.get_sysstat()


@dataclass
class BigBlueButtonGroup:
    name: str

    apis: dict = field(default_factory=dict)
    workers: int = 10

    logout_url: Optional[str] = None
    origin: Optional[str] = "python-bigbluebutton2"
    origin_server_name: str = getfqdn()

    generate_meeting_id: Callable[[], str] = lambda: str(uuid1())

    @property
    def meetings(self) -> dict:
        res = {}

        for name, api in self.apis.items():
            res.update(api.meetings)

        return res

    def new(self, name: str, *args, **kwargs) -> BigBlueButton:
        logger.debug(f"Creating new API client {name}")
        bbb = BigBlueButton(self, name, *args, **kwargs)
        return bbb

    def _foreach(self, method: str, *args, **kwargs) -> Dict[str, Any]:
        logger.debug(
            f"Calling method {method} on all servers in group {self.name} ({self.workers} workers)"
        )
        res = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as pool:
            futures = {}
            for name, bbb in self.apis.items():
                fn = getattr(bbb, method)
                futures[pool.submit(fn, *args, **kwargs)] = name
                logger.debug(f"Pooled method {method} on server {name}")

            logger.debug("Waiting for pooled methods")
            for future in concurrent.futures.as_completed(futures):
                name = futures[future]
                res[name] = future.result()
                logger.debug(f"Pooled method {method} on server {name} returned")

        return res

    def get_meetings(self) -> Dict[str, "Meeting"]:
        self._foreach("get_meetings")
        return self.meetings

    def ssh_command(
        self, command: Sequence[str], input_: Optional[str] = None
    ) -> Dict[str, subprocess.CompletedProcess]:
        res = self._foreach("ssh_command", command, input_)
        return res

    def get_sysstat(self):
        res = self._foreach("get_sysstat")
        return res

    def refresh(self):
        res = self._foreach("refresh")
        return res

    def select_api(self, **kwargs):
        # Start with a ranking of 10 for each API
        apis = {api_name: 10.0 for api_name in self.apis}

        # Define checkers to run on each API
        # Each checker returns a factor to scale the ranking by
        checkers = lb_checkers

        # Apply checkers, in order
        for checker in checkers:
            for api_name, ranking in apis.items():
                factor = checker(self.apis[api_name], **kwargs)
                apis[api_name] *= factor

        # Get maximum ranking and all APIs that got it
        max_ranking = max(apis.values())
        apis_won = [
            self.apis[api_name] for api_name, ranking in apis.items() if ranking == max_ranking
        ]

        # Select random API from winners
        api = random.choice(apis_won)  # noqa: S311, not cryptographic
        return api

    def create_meeting(self, do_create=True, *args, **kwargs) -> Meeting:
        meeting_id = kwargs.get("meeting_id")
        if meeting_id and (meeting_id in self.meetings or meeting_id in self.get_meetings()):
            api = self.meetings[meeting_id].api
            logger.info(f"Found meeting with id {meeting_id} on server {api.name}")
        else:
            logger.info(f"Creating new meeting on one server in group {self.name}")
            api = self.select_api()

        return api.create_meeting(do_create, *args, **kwargs)

    def _find_meeting(self, meeting_id: str) -> Optional[Meeting]:
        if meeting_id in self.meetings or meeting_id in self.get_meetings():
            return self.meetings[meeting_id]
        return None

    def is_meeting_running(self, meeting_id: str) -> bool:
        meeting = self._find_meeting(meeting_id)
        if meeting:
            return meeting.is_meeting_running()
        else:
            return False

    def end_meeting(self, meeting_id: str, password: Optional[str] = None) -> bool:
        meeting = self._find_meeting(meeting_id)
        if meeting:
            # Verify password before even sending the call, if provided
            # Entirely useless because anyone who can call end can also call getMeetingInfo,
            # but let's play along…
            if password is not None and password != meeting.moderator_pw:
                raise ValueError("The supplied moderatorpassword does not match.")
            return meeting.end()

    def handle_from_data(
        self,
        method: str,
        attrs: Optional[dict] = None,
        content: Optional[str] = None,
        filter_meta: Optional[dict] = None,
    ) -> dict:
        if not attrs:
            attrs = {}

        if method == "create":
            kwargs = Meeting.get_kwargs_from_url_args(attrs)
            meeting = self.create_meeting(**kwargs)

            return meeting.to_dict()
        elif method == "join":
            meeting = self._find_meeting(attrs["meetingID"])
            if meeting:
                kwargs = Attendee.get_kwargs_from_url_args(attrs, meeting)
                attendee = Attendee(meeting=meeting, **kwargs)
                attendee.join()

                # We need to construct this one response manually, because for some inobvious
                # reason the designers of the BBB API changed their minds and started using
                # snake_case instead of dromedarCase
                return {
                    "meeting_id": meeting.meeting_id,
                    "user_id": attendee.user_id,
                    "auth_token": attendee.auth_token,
                    "session_token": attendee.session_token,
                    "url": attendee.url,
                }
            else:
                raise KeyError("Meeting not found.")
        elif method == "isMeetingRunning":
            running = self.is_meeting_running(attrs["meetingID"])
            return {"running": "true" if running else "false"}
        elif method == "end":
            self.end_meeting(attrs["meetingID"], attrs["password"])
            return {}
        elif method == "getMeetingInfo":
            meeting = self._find_meeting(attrs["meetingID"])
            if meeting:
                meeting.get_meeting_info()
                return meeting.to_dict()
            else:
                raise KeyError("Meeting not found.")
        elif method == "getMeetings":
            meetings = self.get_meetings()
            return {
                "meetings": [
                    {"meeting": meeting.to_dict()} for meeting_id, meeting in meetings.items()
                ]
            }
        elif method == "getRecordings":
            raise NotImplementedError(f"Method {method} not implemented yet")
        elif method == "publishRecordings":
            raise NotImplementedError(f"Method {method} not implemented yet")
        elif method == "deleteRecordings":
            raise NotImplementedError(f"Method {method} not implemented yet")
        elif method == "updateRecordings":
            raise NotImplementedError(f"Method {method} not implemented yet")
        elif method == "getDefaultConfigXML":
            raise NotImplementedError(f"Method {method} not implemented yet")
        elif method == "setConfigXML":
            raise NotImplementedError(f"Method {method} not implemented yet")
        elif method == "getRecordingTextTracks":
            raise NotImplementedError(f"Method {method} not implemented yet")
        elif method == "PutRecordingTextTrack":
            raise NotImplementedError(f"Method {method} not implemented yet")
        else:
            raise TypeError(f"Method {method} is unknown")
