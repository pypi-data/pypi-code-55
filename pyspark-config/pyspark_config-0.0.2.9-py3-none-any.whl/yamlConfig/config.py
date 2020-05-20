"""This module implements abstract config class."""
from abc import ABCMeta
from dataclasses import dataclass
from pathlib import Path
from typing import (Any, Union,Type, Optional)
import yaml
import os
import warnings
from future.utils import raise_from
from enum import Enum
from marshmallow import post_load, Schema
from pyspark_config.errors import *

from dataclasses_json import DataClassJsonMixin
from dataclasses_json.cfg import config
from dataclasses_json.mm import (SchemaType, build_schema, schema)
from dataclasses_json.undefined import Undefined
from dataclasses_json.utils import (_undefined_parameter_action_safe, _get_type_cons,
                                    _handle_undefined_parameters_safe,
                                    _is_collection, _is_mapping, _is_new_type,
                                    _is_optional, _issubclass_safe, CatchAllVar)
from dataclasses_json.core import (_user_overrides_or_exts, get_type_hints,
                                   _decode_letter_case_overrides,
                                   _is_supported_generic,
                                   _support_extended_types,
                                   _decode_dict_keys, _ExtendedEncoder,
                                   _decode_generic,
                                   _decode_items)

from dataclasses_json.api import A
from dataclasses import (MISSING,
                         fields,
                         is_dataclass  # type: ignore
                         )

Json = Union[dict, list, str, int, float, bool, None]
from pyspark_config.yamlConfig import create_file_path_field, build_path

def build_schema(cls: Type[A],
                 mixin,
                 infer_missing,
                 partial) -> Type[SchemaType]:
    Meta = type('Meta',
                (),
                {'fields': tuple(field.name for field in fields(cls)
                                 if
                                 field.name != 'dataclass_json_config' and field.type !=
                                 Optional[CatchAllVar]),
                 # TODO #180
                 # 'render_module': global_config.json_module
                 })

    @post_load
    def make_instance(self, kvs, **kwargs):
        return _decode_dataclass(cls, kvs, partial)

    def dumps(self, *args, **kwargs):
        if 'cls' not in kwargs:
            kwargs['cls'] = _ExtendedEncoder

        return Schema.dumps(self, *args, **kwargs)

    def dump(self, obj, *, many=None):
        dumped = Schema.dump(self, obj, many=many)
        # TODO This is hacky, but the other option I can think of is to generate a different schema
        #  depending on dump and load, which is even more hacky

        # The only problem is the catch all field, we can't statically create a schema for it
        # so we just update the dumped dict
        if many:
            for i, _obj in enumerate(obj):
                dumped[i].update(
                    _handle_undefined_parameters_safe(cls=_obj, kvs={},
                                                      usage="dump"))
        else:
            dumped.update(_handle_undefined_parameters_safe(cls=obj, kvs={},
                                                            usage="dump"))
        return dumped

    schema_ = schema(cls, mixin, infer_missing)
    DataClassSchema: Type[SchemaType] = type(
        f'{cls.__name__.capitalize()}Schema',
        (Schema,),
        {'Meta': Meta,
         f'make_{cls.__name__.lower()}': make_instance,
         'dumps': dumps,
         'dump': dump,
         **schema_})

    return DataClassSchema


@dataclass
class DataClassJsonMix(DataClassJsonMixin):

    @classmethod
    def schema(cls: Type[A],
               *,
               infer_missing: bool = False,
               only=None,
               exclude=(),
               many: bool = False,
               context=None,
               load_only=(),
               dump_only=(),
               partial: bool = False,
               unknown=None) -> SchemaType:
        Schema = build_schema(cls, DataClassJsonMix, infer_missing, partial)

        if unknown is None:
            undefined_parameter_action = _undefined_parameter_action_safe(cls)
            if undefined_parameter_action is not None:
                # We can just make use of the same-named mm keywords
                unknown = undefined_parameter_action.name.lower()

        return Schema(only=only,
                      exclude=exclude,
                      many=many,
                      context=context,
                      load_only=load_only,
                      dump_only=dump_only,
                      partial=partial,
                      unknown=unknown)

    @classmethod
    def from_dict(cls: Type[A],
                  kvs: Json,
                  *,
                  infer_missing=False) -> A:
        return _decode_dataclass(cls, kvs, infer_missing)


def dataclass_json(_cls=None, *, letter_case=None,
                   undefined: Optional[Union[str, Undefined]] = None):
    """
    Based on the code in the `dataclasses` module to handle optional-parens
    decorators. See example below:

    @dataclass_json
    @dataclass_json(letter_case=Lettercase.CAMEL)
    class Example:
        ...
    """

    def wrap(cls):
        return _process_class(cls, letter_case, undefined)

    if _cls is None:
        return wrap
    return wrap(_cls)


def _process_class(cls, letter_case, undefined):
    if letter_case is not None or undefined is not None:
        cls.dataclass_json_config = config(letter_case=letter_case,
                                           undefined=undefined)[
            'dataclasses_json']

    cls.to_json = DataClassJsonMix.to_json
    # unwrap and rewrap classmethod to tag it to cls rather than the literal
    # DataClassJsonMixin ABC
    cls.from_json = classmethod(DataClassJsonMix.from_json.__func__)
    cls.to_dict = DataClassJsonMix.to_dict
    cls.from_dict = classmethod(DataClassJsonMix.from_dict.__func__)
    cls.schema = classmethod(DataClassJsonMix.schema.__func__)

    cls.__init__ = _handle_undefined_parameters_safe(cls, kvs=(), usage="init")
    # register cls as a virtual subclass of DataClassJsonMixin
    DataClassJsonMixin.register(cls)
    return cls


def _decode_dataclass(cls, kvs, infer_missing):
    if isinstance(kvs, cls):
        return kvs
    overrides = _user_overrides_or_exts(cls)
    kvs = {} if kvs is None and infer_missing else kvs
    field_names = [field.name for field in fields(cls)]
    decode_names = _decode_letter_case_overrides(field_names, overrides)
    kvs = {decode_names.get(k, k): v for k, v in kvs.items()}
    missing_fields = {field for field in fields(cls) if field.name not in kvs}

    for field in missing_fields:
        if field.default is not MISSING:
            kvs[field.name] = field.default
        elif field.default_factory is not MISSING:
            kvs[field.name] = field.default_factory()
        elif infer_missing:
            kvs[field.name] = None

    # Perform undefined parameter action
    kvs = _handle_undefined_parameters_safe(cls, kvs, usage="from")

    init_kwargs = {}
    types = get_type_hints(cls)
    for field in fields(cls):
        # The field should be skipped from being added
        # to init_kwargs as it's not intended as a constructor argument.
        if not field.init:
            continue

        from typing import GenericMeta
        field_value = kvs[field.name]
        field_type = types[field.name]
        if _is_supported_generic(field_type) and field_type.__args__[0]!=str:
            type_param = 'type' in [f.name for f in fields(field_type.__args__[0])]
        elif 'type' in field_names:
            type_param = True
        else:
            type_param = False


        if field_value is None and not _is_optional(field_type):
            warning = (f"value of non-optional type {field.name} detected "
                       f"when decoding {cls.__name__}")
            if infer_missing:
                warnings.warn(
                    f"Missing {warning} and was defaulted to None by "
                    f"infer_missing=True. "
                    f"Set infer_missing=False (the default) to prevent this "
                    f"behavior.", RuntimeWarning)
            else:
                pass
            init_kwargs[field.name] = field_value
            continue

        while True:
            if not _is_new_type(field_type):
                break

            field_type = field_type.__supertype__

        if (field.name in overrides
                and overrides[field.name].decoder is not None):
            # FIXME hack
            if field_type is type(field_value):
                init_kwargs[field.name] = field_value
            else:
                init_kwargs[field.name] = overrides[field.name].decoder(
                    field_value)
        elif is_dataclass(field_type):
            # FIXME this is a band-aid to deal with the value already being
            # serialized when handling nested marshmallow schema
            # proper fix is to investigate the marshmallow schema generation
            # code
            if is_dataclass(field_value):
                value = field_value
            else:
                value = _decode_dataclass(field_type, field_value,
                                          infer_missing)
            init_kwargs[field.name] = value
        elif _is_supported_generic(field_type) and field_type != str and not type_param:
            init_kwargs[field.name] = _decode_generic(field_type,
                                                      field_value,
                                                      infer_missing)

        elif _is_supported_generic(field_type) and field_type.__args__[0] != str and type_param:
            init_kwargs[field.name] = _decode_generic_subsets(field_type,
                                                      field_value,
                                                      infer_missing)
        else:
            init_kwargs[field.name] = _support_extended_types(field_type,
                                                              field_value)

    return cls(**init_kwargs)


def _decode_generic_subsets(type_, value, infer_missing):
    if value is None:
        res = value
    elif _issubclass_safe(type_, Enum):
        # Convert to an Enum using the type as a constructor.
        # Assumes a direct match is found.
        res = type_(value)
    # FIXME this is a hack to fix a deeper underlying issue. A refactor is due.
    elif _is_collection(type_):
        if _is_mapping(type_):
            k_type, v_type = getattr(type_, "__args__", (Any, Any))
            # a mapping type has `.keys()` and `.values()`
            # (see collections.abc)
            ks = _decode_dict_keys(k_type, value.keys(), infer_missing)
            vs = _decode_items(v_type, value.values(), infer_missing)
            xs = zip(ks, vs)
        else:
            xs = (_decode_dataclass(getSubclass(type_,v), v, infer_missing)
                  for v in value)

        # get the constructor if using corresponding generic type in `typing`
        # otherwise fallback on constructing using type_ itself
        try:
            res = _get_type_cons(type_)(xs)
        except (TypeError, AttributeError):
            res = type_(xs)
    else:  # Optional or Union
        if not hasattr(type_, "__args__"):
            # Any, just accept
            res = value
        elif _is_optional(type_) and len(type_.__args__) == 2:  # Optional
            type_arg = type_.__args__[0]
            if is_dataclass(type_arg) or is_dataclass(value):
                res = _decode_dataclass(type_arg, value, infer_missing)
            elif _is_supported_generic(type_arg):
                res = _decode_generic(type_arg, value, infer_missing)
            else:
                res = _support_extended_types(type_arg, value)
        else:  # Union (already decoded or unsupported 'from_json' used)
            res = value
    return res


def getSubclass(cls, values):
    """
    In case one of the fields is called type, the corresponding
    subclass is searched for.
    """
    try:
        subclass_map = {subclass.type: subclass for subclass
                        in cls.__args__[0].__subclasses__()}
    except:
        raise
    try:
        return subclass_map[values['type']]
    except KeyError:
        raise Exception("Type "+values['type']+" not available.")


@dataclass
class YamlDataClassConfig(DataClassJsonMix, metaclass=ABCMeta):
    """This class implements YAML file load function."""

    def load(self, path: str, path_is_absolute: bool = False):
        """
        This method loads from YAML file to properties of self instance.
        Args:
          path: The path in string form; can be relative or absolute.
          path_is_absolute: indicates whether the path is an absolute path
        """
        path_type=Path(path)
        built_path = build_path(path_type, path_is_absolute)
        if os.path.exists(path):
            if path.endswith('.yaml'):
                with built_path.open('r', encoding='UTF-8') as yml:
                    dictionary_config = yaml.load(yml)
            else:
                raise InvalidTypeError("Configuration file must "
                                       "be in YAML format: %s"
                                        % str(built_path))
        else:
            raise NotFoundError("No such file or directory: %s"
                                     % str(built_path))

        self.__dict__.update(
            self.schema().load(dictionary_config).__dict__
        )