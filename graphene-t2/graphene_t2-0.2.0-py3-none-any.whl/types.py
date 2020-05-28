import graphene
import graphene_django
from graphene.pyutils.init_subclass import InitSubclassMeta

from .features import changes, ordering, required, model_info
from .options import (
    DjangoObjectTypeOptions,
    InputObjectOptions,
    QueriesOptions,
)
from .utils import (
    get_fields,
    get_t2meta_cls,
    get_t2meta_obj,
    t2meta_cls_to_obj,
)


def _init_options(cls, options_cls):
    super_opts = get_t2meta_obj(cls)
    t2meta_cls = get_t2meta_cls(cls)
    opts = options_cls.from_meta(t2meta_cls).merge(super_opts)
    t2meta_cls_to_obj(cls, opts)
    return opts


class InputObjectType(graphene.InputObjectType):
    data_converters = {}

    @classmethod
    def apply_converters(cls, input_data):
        prepared_data = {}
        for field, value in input_data.items():
            func = cls.data_converters.get(field)
            prepared_data[field] = func(value) if func else value

        return prepared_data

    @classmethod
    def __init_subclass_with_meta__(cls, container=None, _meta=None, **options):
        cls._handle_t2meta(InputObjectOptions)
        super().__init_subclass_with_meta__(container, _meta, **options)

    @classmethod
    def _handle_t2meta(cls, options_cls):
        opts = _init_options(cls, options_cls)
        if opts.abstract:
            return

        own_fields = {}
        fields = get_fields(cls)
        model_info.create_fields(opts, fields, own_fields)
        model_info.update_description(opts, fields, own_fields)
        changes.update_description(opts, fields, own_fields)
        required.apply_required(opts, fields, own_fields)
        for field_name, field in own_fields.items():
            setattr(cls, field_name, field)


class QueriesType(metaclass=InitSubclassMeta):
    def __init_subclass__(cls):
        opts = _init_options(cls, QueriesOptions)
        fields = get_fields(cls)
        ordering.enable_ordering(cls, opts, fields)


class DjangoObjectType(graphene_django.DjangoObjectType):
    class Meta:
        abstract = True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        opts = _init_options(cls, DjangoObjectTypeOptions)
