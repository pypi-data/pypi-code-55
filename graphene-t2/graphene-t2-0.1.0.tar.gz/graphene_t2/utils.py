from graphene import Argument, Field, InputField, List, Scalar

_META_CLS_NAME = "T2Meta"
_META_OBJ_NAME = "_t2meta"


def get_t2meta_cls(cls):
    return getattr(cls, _META_CLS_NAME, None)


def get_t2meta_obj(cls):
    return getattr(cls, _META_OBJ_NAME, None)


def t2meta_cls_to_obj(cls, opts):
    if hasattr(cls, _META_CLS_NAME):
        delattr(cls, _META_CLS_NAME)
    setattr(cls, _META_OBJ_NAME, opts)


def get_resolver(cls, field_name):
    return getattr(cls, f"resolve_{field_name}", None)


def get_fields(cls):
    fields = {}
    for name in dir(cls):
        if name.startswith("_"):
            continue
        attr = getattr(cls, name)
        if isinstance(attr, (Argument, Field, InputField, List, Scalar)):
            fields[name] = attr
    return fields
