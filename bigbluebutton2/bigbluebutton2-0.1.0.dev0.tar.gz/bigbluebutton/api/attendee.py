"""Data structures for manageing meeting attendees"""

import logging
import webbrowser
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .util import camel_to_snake, snake_to_camel, to_field_type

logger = logging.getLogger(__name__)


class Role(Enum):
    """Enumeration of roles an attendee can have"""

    MODERATOR = "MODERATOR"
    VIEWER = "VIEWER"
    DIAL_IN_USER = "DIAL-IN-USER"


@dataclass
class Attendee:
    """One attendee that participates in one meeting.

    This object holds the information about one participant and is linked to
    exactly one meeting.
    """

    meeting: "Meeting"  # noqa: F821
    full_name: str
    user_id: Optional[str] = None
    role: Optional[Role] = None
    is_presenter: bool = False
    is_listening_only: bool = False
    has_joined_voice: bool = False
    has_video: bool = False
    client_type: Optional[str] = None

    auth_token: Optional[str] = None
    session_token: Optional[str] = None
    url: Optional[str] = None

    def __post_init__(self):
        self.meeting.attendees[self.full_name] = self

    def join(self, browser: bool = False) -> str:
        """Ask BigBlueButton to join an attendee corresponding to this object into the meeting
        it is linked to.

        To request the join, this method can either call the API directly and return the URL to
        the (HTML5) client, or only construct the API call URL and then hand it off to the
        default browser (if the browser argument is set to True).

        In BigBlueButton's default configuration, in addition to the session token in the client
        URL, a valid JSESSIONID cookie is required, so using the client URL outside the original
        request scope only works if the server supports it.
        """
        logger.info(
            f"Joining meeting {self.meeting.meeting_id} on server {self.meeting.api.name} "
            f"as {self.full_name}, role {self.role}"
        )

        url_args = {}

        url_args["meetingID"] = self.meeting.meeting_id

        url_args["fullName"] = self.full_name

        if self.user_id:
            url_args["userID"] = self.user_id

        if self.role == Role.MODERATOR:
            url_args["password"] = self.meeting.moderator_pw
        elif self.role == Role.VIEWER:
            url_args["password"] = self.meeting.attendee_pw

        url_args["createTime"] = self.meeting.create_time

        if browser:
            url_args["redirect"] = "true"
            url = self.meeting.api._build_url("join", url_args)

            logger.info("Handing join request off to default browser")
            webbrowser.open(url)
        else:
            url_args["redirect"] = "false"

            logger.debug("Sending join request")
            res = self.meeting.api._request("join", url_args)
            self._update_from_response(res)

        return self.url

    def _update_from_response(self, res):
        for name, value in res.items():
            if name == "role":
                self.role = Role(value)
            else:
                snake_name = camel_to_snake(name)

                if hasattr(self, snake_name):
                    setattr(self, snake_name, to_field_type(self, snake_name, value))

    def to_dict(self, *args, **kwargs):
        res = {}

        for name, value in self.__dict__.items():
            if args and name not in args and name not in kwargs:
                continue

            if name == "meeting":
                res["meetingID"] = self.meeting.meeting_id
            elif value is not None:
                if name in kwargs:
                    camel_name = kwargs[name]
                else:
                    camel_name = snake_to_camel(name)

                if isinstance(value, bool):
                    str_value = "true" if value else "false"
                else:
                    str_value = str(value)

                res[camel_name] = str_value

        return res

    @classmethod
    def get_kwargs_from_url_args(cls, urlargs: dict, meeting: "Meeting") -> dict:
        kwargs = {}

        for name, value in urlargs.items():
            if name == "password":
                # Determine role by used password
                if value == meeting.attendee_pw:
                    kwargs["role"] = Role.VIEWER
                elif value == meeting.moderator_pw:
                    kwargs["role"] = Role.MODERATOR
                else:
                    raise ValueError("Invalid password passed, could not determine role")
            elif name == "meetingID":
                if value != meeting.meeting_id:
                    raise ValueError("Meeting ID does not match")
            elif name == "createTime":
                if int(value) != meeting.create_time:
                    raise ValueError("createTime does not match actual meeting parameters")
            else:
                snake_name = camel_to_snake(name)
                kwargs[snake_name] = to_field_type(cls, snake_name, value)

        return kwargs
