from copy import deepcopy

from graphene import Argument


def apply_required(meta, fields, own_fields):
    required_params = getattr(meta, "required", None)
    if not required_params:
        return
    assert not (set(required_params.keys()) - set([True, False]))

    for is_required, field_names in required_params.items():
        if field_names == "__all__":
            field_names = list(fields.keys())
        _handle_fields(own_fields, fields, field_names, is_required)


def _handle_fields(own_fields, fields, field_names, is_required):
    for name in field_names:
        field = own_fields.get(name) or deepcopy(fields[name])
        own_fields[name] = field
        if not isinstance(field, Argument):
            field.kwargs["required"] = is_required
