from typing import Generic, TypeVar
from enum import Enum

from . import fields
from .base import BaseConfig, CustomField


class LogFormat(CustomField, Enum):
    json = 'json'
    plain = 'plain'

    @property
    def raw(self) -> str:
        return str(self.value).lower()

    @staticmethod
    def serialize(value: str):
        return LogFormat(value.lower())


class LogLevel(CustomField, Enum):
    critical = 'CRITICAL'
    error = 'ERROR'
    warning = 'WARNING'
    info = 'INFO'
    debug = 'DEBUG'
    notset = 'NOTSET'

    @property
    def raw(self) -> str:
        return str(self.value).lower()

    @staticmethod
    def serialize(value: str):
        return LogLevel(value.upper())


class AppConfig(BaseConfig):

    logo = fields.Str(default="""
                                    _
                                   | |
     _ __ ___   __ _  ___ _ __ ___ | |__   __ _ ___  ___
    | '_ ` _ \ / _` |/ __| '__/ _ \| '_ \ / _` / __|/ _ \\
    | | | | | | (_| | (__| | | (_) | |_) | (_| \__ \  __/
    |_| |_| |_|\__,_|\___|_|  \___/|_.__/ \__,_|___/\___|
""")

    version = fields.Str(default='0.0')
    name    = fields.Str(default='macrobase', env_key='NAME')

    # TODO: fix it
    workers = fields.Int(default=1)

    debug       = fields.Bool(default=False)
    log_format  = fields.Custom(LogFormat, default=LogFormat.json)
    log_level   = fields.Custom(LogLevel, default=LogLevel.debug)


class DriverConfig(BaseConfig):

    logo = fields.Str(default="""
 _____       _
|  __ \     (_)
| |  | |_ __ ___   _____ _ __
| |  | | '__| \ \ / / _ \ '__|
| |__| | |  | |\ V /  __/ |
|_____/|_|  |_| \_/ \___|_|
""")


AT = TypeVar('AT')
DT = TypeVar('DT')


class CommonConfig(Generic[AT, DT]):

    def __init__(self, app_config: AT, driver_config: DT):
        self._app = app_config
        self._driver = driver_config

    @property
    def app(self) -> AT:
        return self._app

    @property
    def driver(self) -> DT:
        return self._driver
