"""Create fields on-the-fly at form construction time."""

from inspect import getmembers, ismethod
from typing import Callable, Protocol, Dict, Any, Sequence

from wtforms import Field
from wtforms.form import BaseForm
from wtforms.meta import DefaultMeta

__version__ = "0.1"


class _FieldFactory(Protocol):
    field_name: str
    is_enabled: Callable[..., bool]

    def __call__(self, *args, **kwargs) -> Field:
        pass


class EnableIfFunction(Protocol):
    """Create this field at construction time only if the given criteria is fulfilled. The arguments
    are the same passed to the actual field factory.
    """

    def __call__(self, *args, **kwargs) -> bool:
        pass


def field(name: str, enable_if: EnableIfFunction = None):
    """Mark a callable as form field factory. By default, it is enabled."""

    def decorator(function: _FieldFactory):
        function.field_name = name
        function.is_enabled = enable_if or (lambda *args, **kwargs: True)  # type: ignore
        return function

    return decorator


def _get_underlying_func(callable_):
    try:
        return callable_.__func__
    except AttributeError:
        return callable_


class Form(BaseForm):
    """Keyword arguments represent those from ``wtforms.form.BaseForm.process``. To control which
    data is sent to the field factories, derive from this class and call ``set_factory_args()``
    prior to ``super().__init__``. You need to do this anyway to have a form framework (with the
    meta setup to e.g. use CSRF and a specific locale) tailored to your use case. If you use an
    instance method as a field, you can also directly use ``self`` as a way to pass state. The
    ``enable_if`` callable is then also supplied with the ``self`` argument.
    """

    _factory_args: Sequence[Any] = ()
    _factory_kwargs: Dict[str, Any] = {}

    def __init__(self, prefix="", meta=DefaultMeta(), **kwargs):
        # bind fields within wtforms
        super().__init__(tuple(self._gen_fields()), prefix, meta)
        # easy access to fields via "form.<field_name>" in e.g. templates
        self._make_field_attributes()
        # process the passed form data during construction time for convenience
        self.process(**kwargs)

    def set_factory_args(self, *args, **kwargs):
        """Set the arguments passed to the field factories."""
        self._factory_args = args
        self._factory_kwargs = kwargs

    def _gen_factories(self):
        for _, factory in getmembers(self):
            if callable(factory):
                underlying = _get_underlying_func(factory)
                if hasattr(underlying, "field_name"):
                    yield underlying, factory

    def _gen_fields(self):
        for underlying, factory in self._gen_factories():
            extra_args = (factory.__self__,) if ismethod(factory) else ()
            if underlying.is_enabled(*(extra_args + self._factory_args), **self._factory_kwargs):
                yield (underlying.field_name, factory(*self._factory_args, **self._factory_kwargs))

    def _make_field_attributes(self):
        for name, fld in self._fields.items():
            setattr(self, name, fld)
