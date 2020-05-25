"""Deserializer factory for a generic class."""

import inspect
import sys
import typing
from functools import partial
from typing import (
    Any,
    Callable,
    Dict,
    FrozenSet,
    List,
    Mapping,
    Sequence,
    Type,
    TypeVar,
)

import attr

from . import combinators, factories, iterator_utils, metadata
from .errors import (
    ErrorDisplayStrategy,
    InternalDeserializationError,
    InternalDeserializerFactoryError,
)
from .pretty_printer import print_type_name
from .types import DeserializableType, Deserializer, Primitive, T

S = TypeVar("S")


class ClassDeserializationError(InternalDeserializationError):
    """Raised when a primitive cannot be deserialized into a class."""


@attr.s(auto_attribs=True, frozen=True)
class ClassValueDeserializer(Deserializer[T]):
    """Deserialize a class from a single value."""

    _target_t: DeserializableType
    _handle_exception_ts: FrozenSet[Type[Exception]]
    _fn: Callable[..., T]
    _value_deserializer: Deserializer

    def __call__(self, value: Primitive) -> T:
        """Deserialize a primitive into parameters for a function call."""
        try:
            arg = self._value_deserializer(value)
        except InternalDeserializationError as e:
            raise ClassDeserializationError(
                value,
                self._fn,
                cause=e,
                display_strategy=ErrorDisplayStrategy.ALWAYS_COLLAPSE,
            )
        try:
            return self._fn(arg)
        except tuple(  # pylint: disable=catching-non-exception
            self._handle_exception_ts
        ) as e:
            raise ClassDeserializationError(
                value,
                self._fn,
                cause=e,
                display_strategy=ErrorDisplayStrategy.EAGERLY_COLLAPSE,
            )


class ClassDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when failing to create a class deserializer."""


@attr.s(auto_attribs=True, frozen=True)
class ClassDeserializerFactory(factories.TypeDeserializerFactory):
    """Create deserializer for a class."""

    _enable_if: Callable[[DeserializableType], bool] = lambda _: True
    _handle_exception_ts: FrozenSet[Type[Exception]] = attr.ib(factory=frozenset)

    def create_deserializer(
        self,
        recurse_factory: factories.InternalDeserializerFactory,
        type_: DeserializableType,
    ) -> Deserializer[T]:
        """Create a deserializer for the specified class type."""
        if not self._enable_if(type_):
            raise ClassDeserializerFactoryError(
                type_, f"disabled for type '{print_type_name(type_)}'"
            )
        if not hasattr(type_, "__call__"):
            raise ClassDeserializerFactoryError(type_, "not a callable type")

        parameters = _get_parameters(type_)
        class_deserializers = {}
        errors = {}
        for desc, fn in {
            "from dict": _create_class_dict_deserializer,
            "from list": _create_class_list_deserializer,
            "from value": _create_class_value_deserializer,
        }.items():
            try:
                class_deserializers[desc] = fn(
                    self._handle_exception_ts, recurse_factory, type_, parameters
                )
            except InternalDeserializerFactoryError as e:
                errors[desc] = e
        if class_deserializers:
            return combinators.OneOfDeserializer(
                type_,
                class_deserializers,
                partial(
                    ClassDeserializationError,
                    display_strategy=ErrorDisplayStrategy.ALWAYS_DISPLAY,
                ),
            )
        raise ClassDeserializerFactoryError(
            type_, ClassDeserializerFactoryError.cannot_create_msg("class"), errors
        )


def _create_class_value_deserializer(
    handle_exception_ts: FrozenSet[Type[Exception]],
    recurse_factory: factories.InternalDeserializerFactory,
    type_: DeserializableType,
    parameters: Sequence["_Parameter"],
) -> Deserializer:
    required, optional = iterator_utils.divide_list(_Parameter.is_required, parameters)
    if len(required) > 1 or len(required) + len(optional) < 1:
        raise ClassDeserializerFactoryError(
            type_,
            "unsupported number of parameters "
            "(required: {}, optional: {})".format(len(required), len(optional)),
        )

    value_parameter = parameters[0]
    if not value_parameter.is_pos():
        raise ClassDeserializerFactoryError(
            type_, "non-positional first parameter {}".format(value_parameter.name),
        )
    return ClassValueDeserializer(
        type_,
        handle_exception_ts,
        type_,
        _get_deserializers(recurse_factory, type_, [value_parameter])[
            value_parameter.name
        ],
    )


def _create_class_list_deserializer(
    handle_exception_ts: FrozenSet[Type[Exception]],
    recurse_factory: factories.InternalDeserializerFactory,
    type_: DeserializableType,
    parameters: Sequence["_Parameter"],
) -> Deserializer:
    non_pos_required = [
        p.name for p in parameters if p.is_required() and not p.is_pos()
    ]
    if non_pos_required:
        raise ClassDeserializerFactoryError(
            type_,
            "required non-positional parameter(s) {}".format(
                ", ".join(non_pos_required)
            ),
        )

    pos = [p for p in parameters if p.is_pos()]
    deserializers = _get_deserializers(recurse_factory, type_, pos)
    var_pos, non_var_pos = iterator_utils.divide_list(_Parameter.is_var, pos)

    def construct_fn(value: Primitive, args: Sequence[Any]) -> T:
        try:
            return type_(*args)
        except tuple(  # pylint: disable=catching-non-exception
            handle_exception_ts
        ) as e:
            raise ClassDeserializationError(
                value,
                type_,
                cause=e,
                display_strategy=ErrorDisplayStrategy.EAGERLY_COLLAPSE,
            )

    return combinators.SequenceDeserializer(
        type_,
        recurse_factory.create_type_deserializer(list),
        [deserializers[p.name] for p in non_var_pos if p.is_required()],
        [deserializers[p.name] for p in non_var_pos if not p.is_required()],
        iterator_utils.get_single_element([deserializers[p.name] for p in var_pos]),
        construct_fn,
        partial(
            ClassDeserializationError,
            display_strategy=ErrorDisplayStrategy.EAGERLY_COLLAPSE,
        ),
    )


def _create_class_dict_deserializer(
    handle_exception_ts: FrozenSet[Type[Exception]],
    recurse_factory: factories.InternalDeserializerFactory,
    type_: DeserializableType,
    parameters: Sequence["_Parameter"],
) -> Deserializer:
    non_kw_required = [p.name for p in parameters if p.is_required() and not p.is_kw()]
    if non_kw_required:  # pragma: no cover TODO
        raise ClassDeserializerFactoryError(
            type_,
            "required non-keyword parameter(s) {}".format(", ".join(non_kw_required)),
        )

    kw = [p for p in parameters if p.is_kw()]
    deserializers = _get_deserializers(recurse_factory, type_, kw)
    var_kw, non_var_kw = iterator_utils.divide_list(_Parameter.is_var, kw)

    def construct_fn(value: Primitive, args: Mapping[str, Any]) -> T:
        try:
            return type_(**args)
        except tuple(  # pylint: disable=catching-non-exception
            handle_exception_ts
        ) as e:
            raise ClassDeserializationError(
                value,
                type_,
                cause=e,
                display_strategy=ErrorDisplayStrategy.EAGERLY_COLLAPSE,
            )

    return combinators.MappingDeserializer(
        type_,
        recurse_factory.create_type_deserializer(dict),
        recurse_factory.create_type_deserializer(str),
        {p.name: deserializers[p.name] for p in non_var_kw if p.is_required()},
        {p.name: deserializers[p.name] for p in non_var_kw if not p.is_required()},
        iterator_utils.get_single_element([deserializers[p.name] for p in var_kw]),
        construct_fn,
        partial(
            ClassDeserializationError,
            display_strategy=ErrorDisplayStrategy.EAGERLY_COLLAPSE,
        ),
    )


@attr.s(auto_attribs=True, frozen=True)
class _Parameter:
    parameter: inspect.Parameter
    metadata: metadata.InternalMetadata

    @property
    def name(self) -> str:
        return self.parameter.name

    def is_var(self) -> bool:
        return self.parameter.kind in {
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        }

    def is_pos(self) -> bool:
        return self.parameter.kind in {
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.VAR_POSITIONAL,
        }

    def is_kw(self) -> bool:
        return self.parameter.kind in {
            inspect.Parameter.KEYWORD_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.VAR_KEYWORD,
        }

    def is_required(self) -> bool:
        return self.parameter.default == inspect.Parameter.empty and not self.is_var()


def _get_parameters(type_: DeserializableType) -> List[_Parameter]:
    try:
        return [
            _Parameter(p, metadata.get_member_metadata(type_, p.name))
            for p in inspect.signature(type_).parameters.values()
        ]
    except ValueError as e:
        raise ClassDeserializerFactoryError(
            type_,
            ClassDeserializerFactoryError.cannot_create_msg("class"),
            e,
            display_strategy=ErrorDisplayStrategy.ALWAYS_DISPLAY,
        )


def _get_deserializers(
    recurse_factory: factories.InternalDeserializerFactory,
    type_: DeserializableType,
    parameters: List[_Parameter],
) -> Dict[str, Deserializer]:
    type_hints = _get_type_hints(type_, [p.parameter for p in parameters])

    def _get_deserializer(parameter: _Parameter) -> Deserializer[T]:
        # Ideally we'd check that deserialize_with targets the right type, but
        # that's nontrivial - issubclass can't handle non-class parameters e.g.
        # unions.
        ds = parameter.metadata.deserialize_with(recurse_factory)
        if ds:
            return ds
        return recurse_factory.create_type_deserializer(type_hints[parameter.name])

    deserializers, errors = iterator_utils.accumulate_errors_d(
        InternalDeserializerFactoryError,
        {parameter.name: (_get_deserializer, parameter) for parameter in parameters},
    )

    if errors:
        raise ClassDeserializerFactoryError(
            type_,
            ClassDeserializerFactoryError.cannot_create_msg("class"),
            {f'parameter "{k}"': e for k, e in errors.items()},
        )
    return deserializers


def _get_type_hints(
    type_: DeserializableType, params: Sequence[inspect.Parameter]
) -> Dict[str, Any]:
    if hasattr(type_, "__globals__"):
        globals_ = getattr(type_, "__globals__")
    elif hasattr(type_, "__module__"):
        globals_ = vars(sys.modules[getattr(type_, "__module__")])
    else:  # pragma: no cover TODO
        globals_ = {}

    # For some reason `get_type_hints` can't handle the type returned by
    # `functools.partial` - but it _can_ handle its `__call__` method.
    if isinstance(type_, partial):
        type_ = type_.__call__

    try:
        type_hints = typing.get_type_hints(type_, globals_)
    except TypeError as e:  # pragma: no cover
        raise ClassDeserializerFactoryError(
            type_, ClassDeserializerFactoryError.cannot_create_msg("class"), e
        )

    def get_type_hint(p: inspect.Parameter) -> Any:
        if p.name in type_hints:
            return type_hints[p.name]
        if p.annotation == inspect.Parameter.empty:
            return Any
        if not isinstance(p.annotation, str):
            return p.annotation
        # TODO __closure__?
        return eval(  # pragma: no cover, pylint: disable=eval-used
            p.annotation, globals_
        )

    return {p.name: get_type_hint(p) for p in params}
