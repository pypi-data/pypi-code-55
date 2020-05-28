from copy import deepcopy

import graphene
from django.core.exceptions import FieldDoesNotExist
from django.db.models import CharField, ForeignKey, Model, TextField
from graphene_django.converter import convert_django_field

from . import required as feature_required


def update_description(meta, fields, own_fields):
    if not meta.model:
        return
    assert issubclass(meta.model, Model)

    field_names = tuple(dict(fields, **own_fields).keys())

    for name in field_names:
        try:
            model_field = meta.model._meta.get_field(name)
        except FieldDoesNotExist:
            continue

        is_changed = False
        field = own_fields.get(name) or fields.get(name)
        if not field or not hasattr(field, "kwargs"):
            continue
        description = field.kwargs.get("description", "")
        if not description:
            description = model_field.help_text or model_field.verbose_name or ""
            is_changed = bool(description)

        if isinstance(model_field, (CharField, TextField)):
            len_info = f"Длина (max): {model_field.max_length or 'не ограничена'}"
            description = f"{description + '. ' if description else ''}{len_info}"
            is_changed = True

        if is_changed:
            field = own_fields.get(name) or deepcopy(fields[name])
            field.kwargs["description"] = description
            own_fields[name] = field


def create_fields(meta, fields, own_fields):
    if not (meta.fields and meta.model):
        return

    for name in meta.fields:
        field = own_fields.get(name) or fields.get(name)
        if field:
            continue
        model_field = meta.model._meta.get_field(name)
        if isinstance(model_field, ForeignKey) and name.endswith("_id"):
            field = graphene.ID()
        else:
            field = convert_django_field(model_field)
        own_fields[name] = field

    feature_required.transform_fields(own_fields, fields, meta.required_fields, True)
