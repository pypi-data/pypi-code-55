from functools import wraps

from django.db.models import QuerySet
from graphene import List, String

from ..utils import get_resolver, get_t2meta_obj

_ARG_NAME = "sort_by"


def enable_ordering(cls, meta, fields):
    enable_for = getattr(meta, "enable_ordering_for", None)
    if not enable_for:
        return
    if enable_for == "__auto__":
        enable_for = _search_supported_items(fields)

    for field_name in enable_for:
        _add_ordering_kwargs(fields[field_name])
        _decorate_resolver(cls, fields, field_name)


def _orderator(options):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ordering = kwargs.pop(_ARG_NAME, options.default_ordering)
            qs = func(*args, **kwargs)
            if (
                isinstance(qs, QuerySet)
                and ordering
                and options.validate_ordering(ordering)
            ):
                qs = qs.order_by(*ordering)
            return qs

        return wrapper

    return inner


def _decorate_resolver(cls, fields, field_name):
    field = fields[field_name]
    options = get_t2meta_obj(field.of_type)
    resolver = get_resolver(cls, field_name)
    decorated = _orderator(options)(resolver)
    setattr(cls, resolver.__name__, decorated)


def _add_ordering_kwargs(field):
    field.kwargs[_ARG_NAME] = List(String, description="Список полей для сортировки",)


def _search_supported_items(fields):
    items = []
    for name, field in fields.items():
        if not isinstance(field, List):
            continue
        meta = get_t2meta_obj(field.of_type)
        if meta and hasattr(meta, "can_order_by"):
            items.append(name)

    return items
