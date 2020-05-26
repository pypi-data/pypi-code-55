from copy import deepcopy

from django.core.exceptions import FieldDoesNotExist
from django.db.models import CharField, Model, TextField


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
        field = fields[name]
        if not hasattr(field, "kwargs"):
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
