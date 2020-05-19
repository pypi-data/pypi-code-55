import os
from abc import abstractmethod
from typing import List, Dict, Callable, Any

from macrobase_driver.exceptions import ConfigFileNotFoundException, ConfigFileNotSupportFormatException, ConfigFileParseException


class BaseConfig(object):

    _file_parsers: Dict[str, Callable[[str], dict]] = {}
    # _type_parsers: Dict[Type, Callable[[str], Any]] = {}

    def __init__(self, values: dict = None, file: str = None, *args, **kwargs):
        self._type_properties: Dict[str, Field] = {}

        self._save_types()

        if values is not None:
            self._import_dict(values)
        elif file is not None:
            if not os.path.isfile(file):
                raise ConfigFileNotFoundException

            self._import_file(file)

        self._fill_properties()

    def _save_types(self):
        for p in dir(self):
            attr = getattr(self, p)

            if not self._should_wrap(p) or not isinstance(attr, Field):
                continue

            self._type_properties[p] = attr

    def _fill_properties(self):
        for key, field in self._type_properties.items():
            attr = getattr(self, key)

            if not isinstance(attr, Field):
                continue

            value = field.default

            if field.env_key is not None and field.env_key in os.environ:
                value = field.parse(os.environ.get(field.env_key))

            setattr(self, key, value)

    def _import_file(self, path: str):
        ext = path.split('.')[-1].lower()

        if ext not in self._file_parsers:
            raise ConfigFileNotSupportFormatException

        with open(path, 'rb') as file:
            values = self._file_parsers[ext](file)

        self._import_dict(values)

    def _import_dict(self, values: dict):
        for key, field in self._type_properties.items():
            value = values.get(key)

            if field.env_key is not None and field.env_key in os.environ:
                continue

            if value is None:
                setattr(self, key, field.default)
                continue

            setattr(self, key, field.parse(value))

            # if issubclass(attr.__class__, BaseConfig):
            #     attr._import_dict(values.get(p))
            # else:
            #     if isinstance(attr, list):
            #         if not isinstance(values.get(p), list):
            #             raise ConfigFileParseException(f'Key `{p}` have not match type `list`')
            #
            #         child_types = type_hints.get(p)
            #
            #         if not hasattr(child_types, '__args__') or child_types.__args__ is None or len(child_types.__args__) == 0:
            #             setattr(self, p, values.get(p))
            #             continue
            #
            #         value_type = child_types.__args__[0]
            #         ls = []
            #
            #         for el in values.get(p):
            #             ls.append(self._parse_value(value_type, el))
            #
            #         setattr(self, p, ls)
            #     elif isinstance(attr, dict):
            #         if not isinstance(values.get(p), dict):
            #             raise ConfigFileParseException(f'Key `{p}` have not match type `dict`')
            #
            #         child_types = type_hints.get(p)
            #
            #         if not hasattr(child_types, '__args__') or child_types.__args__ is None or len(child_types.__args__) == 0:
            #             setattr(self, p, values.get(p))
            #             continue
            #
            #         key_type = child_types.__args__[0]
            #         value_type = child_types.__args__[0]
            #         ls = {}
            #
            #         for k, v in values.get(p).items():
            #             key = self._parse_value(key_type, k)
            #             value = self._parse_value(value_type, v)
            #             ls[key] = value
            #
            #         setattr(self, p, ls)
            #     else:
            #         setattr(
            #             self,
            #             p,
            #             self._parse_value(type_hints.get(p), values.get(p))
            #         )

    def _should_wrap(self, name: str) -> bool:
        return not name.startswith('_') and not callable(getattr(self, name))

    # def _parse_value(self, tp: Type, value: str) -> Any:
    #     if type(value) == tp or tp not in self._type_parsers or value is None:
    #         return value
    #
    #     return self._type_parsers.get(tp)(value)

    def set(self, key: str, value: Any):
        setattr(self, key, value)

    @staticmethod
    def file_parser(extensions: List[str]):
        def decorator(parser):
            for ext in extensions:
                BaseConfig._file_parsers[ext] = parser

            return parser

        return decorator


@BaseConfig.file_parser(['yaml', 'yml'])
def yaml_parser(content: str) -> dict:
    from yaml import load, YAMLError
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader

    try:
        return load(content, Loader=Loader)
    except YAMLError as e:
        raise ConfigFileParseException


@BaseConfig.file_parser(['json'])
def json_parser(content: str) -> dict:
    from rapidjson import loads

    try:
        return loads(content)
    except Exception as e:
        raise ConfigFileParseException


class Field:

    def __init__(self, default, env_key: str = None, *args, **kwargs):
        self._default = default
        self._env_key = env_key

    @property
    def default(self):
        return self._default

    @property
    def env_key(self):
        return self._env_key

    @abstractmethod
    def parse(self, value): ...

    @staticmethod
    @abstractmethod
    def parse_value(value): ... # For primitives


class CustomField:

    @staticmethod
    @abstractmethod
    def serialize(value) -> Any:
        pass
