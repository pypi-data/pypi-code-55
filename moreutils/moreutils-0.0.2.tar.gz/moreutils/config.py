"""
moreutils.config
---------------

This is a commonly implemented pattern I use, a singleton Config type that
can handle brick configs (".conf" or ".cfg"), yaml or json configs.

This has a function `.get(*keys, default=None)` which can attempt to get a key
and have an optional default, or `Config['key1', 'key2']` which raises a
`ConfigKeyError` if the config value is not found.

You initialize the config with `Config.load(string_path_or_file_like_object)`
"""
import os
import json
from ast import literal_eval
from copy import deepcopy
from configparser import ConfigParser

import yaml

from .exceptions import ConfigError, ConfigNotLoadedError, ConfigKeyError


def _determine_format(ext):
    ext = ext.lstrip('.')
    if ext.lower() in {'cfg', 'conf', 'config'}:
        return 'cfg'
    if ext.lower() == 'json':
        return 'json'
    if ext.lower() in {'yaml', 'yml'}:
        return 'yaml'
    return None


class _ConfigGetItemMeta(type):
    """
    This metaclass allows you to use getitem on a class itself.
    A bit magical, but allows for an easy way to access config variables.
    """

    def __getitem__(cls, key):
        cls.die_if_not_loaded()
        if isinstance(key, tuple):
            data, found = cls._get(key)
        else:
            data, found = cls._get((key,))
        if not found:
            raise ConfigKeyError(f'cant find config value from keys: {key!r}')
        return data


class Config(metaclass=_ConfigGetItemMeta):
    _CONFIG = None

    def __init__(self, data):
        self._data = data

    @classmethod
    def load(cls, file_or_path, format=None, eval_values=True):
        if isinstance(file_or_path, str) and format is None:
            _, ext = os.path.splitext(file_or_path)
            format = _determine_format(ext)
            if format is None:
                raise ConfigError(
                    f'Could not determine config format from {ext!r}. '
                    f'Please pass an explicit format.'
                )
            with open(file_or_path) as f:
                return cls._load_file(
                    f,
                    format=format,
                    eval_values=eval_values,
                )
        if format is None:
            raise ConfigError(
                'If passing a filelike object, please specify `format` '
                'keyword argument explicitly.'
            )
        return cls._load_file(file_or_path, format=format)

    @classmethod
    def _load_file(cls, _file, *, format, eval_values=True):
        if format == 'cfg':
            return cls._load_brick_format(_file, eval_values=eval_values)
        elif format == 'yaml':
            return cls._load_yaml_format(_file)
        elif format == 'json':
            return cls._load_json_format(_file)
        else:
            raise ConfigError(f'unknown format to parse: {format!r}')

    @classmethod
    def _load_brick_format(cls, _file, eval_values=True):
        conf = ConfigParser()
        conf.read_file(_file)
        section_names = list(conf.sections())
        data = {
            name: dict(conf[name])
            for name in section_names
        }
        if eval_values:
            data = cls._eval_values(data)
        cls._CONFIG = cls(data)
        return cls

    @classmethod
    def _load_yaml_format(cls, _file):
        data = yaml.safe_load(_file)
        cls._CONFIG = cls(data)
        return cls

    @classmethod
    def _load_json_format(cls, _file):
        data = json.load(_file)
        cls._CONFIG = cls(data)
        return cls

    @classmethod
    def _eval_values(cls, data):
        copy = deepcopy(data)
        for sect_name, section in data.items():
            copy_sect = copy[sect_name]
            for key, val in section.items():
                vlow = val.strip().lower()
                if vlow == 'true':
                    copy_sect[key] = True
                    continue
                if vlow == 'false':
                    copy_sect[key] = False
                    continue
                if vlow in ('null', 'none', ''):
                    copy_sect[key] = None
                    continue
                try:
                    copy_sect[key] = literal_eval(val)
                except ValueError:
                    # Keep the string, for example if a value is just `foo`
                    pass
                except SyntaxError:
                    # Keep the string, for example if a value is `!`
                    pass
        return copy

    @classmethod
    def die_if_not_loaded(cls):
        if cls._CONFIG is None:
            raise ConfigNotLoadedError('config not loaded')

    @classmethod
    def _get(cls, keys):
        if not keys:
            raise ConfigError(f'tried Config.get without keys: {keys!r}')
        data = cls._CONFIG._data
        for key in keys:
            if not isinstance(data, dict):
                return None, False
            if key not in data:
                return None, False
            data = data[key]
        return data, True

    @classmethod
    def get(cls, *keys, default=None):
        cls.die_if_not_loaded()
        data, found = cls._get(keys)
        if not found:
            return default
        return data

    @classmethod
    def data(cls):
        cls.die_if_not_loaded()
        return cls._CONFIG._data

    @classmethod
    def is_loaded(cls):
        return bool(cls._CONFIG)

    @classmethod
    def sections(cls):
        cls.die_if_not_loaded()
        return list(cls._CONFIG._data.keys())

    @classmethod
    def items(cls):
        cls.die_if_not_loaded()
        return cls._CONFIG._data.items()
