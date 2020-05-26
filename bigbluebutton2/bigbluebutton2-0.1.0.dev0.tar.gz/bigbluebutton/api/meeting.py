import logging
from dataclasses import dataclass, field
from typing import Dict, Optional

from .attendee import Attendee
from .util import camel_to_snake, snake_to_camel, to_field_type

logger = logging.getLogger(__name__)


@dataclass
class Meeting:
    api: "API"  # noqa: F821
    meeting_id: Optional[str] = None
    meeting_name: Optional[str] = None
    attendee_pw: Optional[str] = None
    moderator_pw: Optional[str] = None
    welcome: Optional[str] = None
    dial_number: Optional[str] = None
    voice_bridge: Optional[str] = None
    max_participants: Optional[int] = None
    logout_url: Optional[str] = None
    record: Optional[bool] = None
    duration: Optional[int] = None
    meta: Dict[str, str] = field(default_factory=dict)
    moderator_only_message: Optional[str] = None
    auto_start_recording: Optional[bool] = None
    allow_start_stop_recording: Optional[bool] = None
    webcams_only_for_moderator: Optional[bool] = None
    logo: Optional[str] = None
    banner_text: Optional[str] = None
    banner_color: Optional[str] = None
    copyright: Optional[str] = None  # noqa: A003
    mute_on_start: Optional[bool] = None
    allow_mods_to_unmute_users: Optional[bool] = None
    lock_settings_disable_cam: Optional[bool] = None
    lock_settings_disable_mic: Optional[bool] = None
    lock_settings_disable_private_chat: Optional[bool] = None
    lock_settings_disable_public_chat: Optional[bool] = None
    lock_settings_disable_note: Optional[bool] = None
    lock_settings_locked_layout: Optional[bool] = None
    lock_settings_lock_on_join: Optional[bool] = None
    lock_settings_lock_on_join_configurable: Optional[bool] = None
    guest_policy: Optional[str] = None

    create_time: int = 0
    running: bool = False
    has_user_joined: bool = False
    recording: bool = False
    has_been_forcibly_ended: bool = False
    start_time: int = 0
    end_time: int = 0
    participant_count: int = 0
    listener_count: int = 0
    voice_participant_count: int = 0
    video_count: int = 0
    max_users: int = 0
    moderator_count: int = 0

    @property
    def origin(self):
        origin = self.meta.get("bbb-origin", "unknown")
        server_name = self.meta.get("bbb-origin-server-name", "")
        return f"{origin} ({server_name})"

    def __post_init__(self):
        self.meeting_id = self.meeting_id or self.api.group.generate_meeting_id()
        self.logout_url = self.logout_url or self.api.group.logout_url

        self.attendees = {}
        self.api.meetings[self.meeting_id] = self

    def create(self):
        # Set origin metadata from API defaults if not defined
        self.meta.setdefault("bbb-origin", self.api.group.origin)
        self.meta.setdefault("bbb-origin-server-name", self.api.group.origin_server_name)

        logger.info(f"Creating meeting {self.meeting_id} on server {self.api.name}")
        res = self.api._request("create", self.get_url_args(meeting_name="name"))
        self._update_from_response(res)

    def is_meeting_running(self):
        res = self.api._request("isMeetingRunning", self.get_url_args("meeting_id"))
        self._update_from_response(res)

        return self.running

    def get_meeting_info(self):
        logger.info(f"Updating information on meeting {self.meeting_id} on server {self.api.name}")
        res = self.api._request("getMeetingInfo", self.get_url_args("meeting_id"))
        self._update_from_response(res)

    def end(self):
        logger.info(f"Ending meeting {self.meeting_id} on server {self.api.name}")
        res = self.api._request("end", self.get_url_args("meeting_id", moderator_pw="password"))
        self._update_from_response(res)

    def to_dict(self, *args, **kwargs) -> dict:
        res = {}

        for name, value in self.__dict__.items():
            if args and name not in args and name not in kwargs:
                continue

            if name == "api":
                continue
            elif name == "meta":
                res["meta"] = self.meta
            elif name == "attendees":
                res["attendees"] = {"attendee": [{full_name: attendee.to_dict() for full_name, attendee in self.attendees.items()}]}
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

    def get_url_args(self, *args, **kwargs) -> dict:
        url_args = self.to_dict(*args, **kwargs)

        if "meta" in url_args:
            # Unpack meta dictionary as values are passed one by one in URL
            for name, value in url_args["meta"].items():
                url_args["meta_" + name] = value
            del url_args["meta"]

        return url_args

    @classmethod
    def get_kwargs_from_url_args(cls, urlargs: dict) -> dict:
        kwargs = {}

        for name, value in urlargs.items():
            if name.startswith("meta_"):
                kwargs.setdefault("meta", {})
                kwargs["meta"][name[5:]] = value
            else:
                snake_name = camel_to_snake(name)
                kwargs[snake_name] = to_field_type(cls, snake_name, value)

        return kwargs

    def _update_from_response(self, res):
        for name, value in res.items():
            if name == "attendees":
                if not value or not value["attendee"]:
                    self.attendees.clear()
                else:
                    if not isinstance(value["attendee"], list):
                        value["attendee"] = [value["attendee"]]

                    for attendee_dict in value["attendee"]:
                        full_name = attendee_dict["fullName"]

                        if full_name in self.attendees:
                            attendee = self.attendees[full_name]
                        else:
                            attendee = Attendee(self, full_name)
                            self.attendees[full_name] = attendee

                        attendee._update_from_response(attendee_dict)
            elif name == "metadata":
                if value:
                    self.meta = dict(value)
                else:
                    self.meta.clear()
            else:
                snake_name = camel_to_snake(name)

                if hasattr(self, snake_name):
                    setattr(self, snake_name, to_field_type(self, snake_name, value))
