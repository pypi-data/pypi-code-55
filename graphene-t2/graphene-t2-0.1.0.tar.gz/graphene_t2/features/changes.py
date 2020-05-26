from copy import deepcopy

from graphene.utils.str_converters import to_camel_case


class AbstractChange:
    def __init__(self, field_name, comment, date_marked, date_to_do=None):
        self.field_name = field_name
        self.comment = comment
        self.date_marked = date_marked
        self.date_to_do = date_to_do

    def __str__(self):
        return f"{self.__class__.__name__}: {self.field_name}"

    def __repr__(self):
        return f"<{self}>"


class Deprecate(AbstractChange):
    def __init__(
        self, field_name, date_marked, date_to_do=None, replaced_by=None, comment=None
    ):
        replaced_by = f"Используйте {to_camel_case(replaced_by)}" if replaced_by else ""
        comment = f'Deprecated. {replaced_by}{". "if replaced_by and comment else ""}{comment or ""}'
        super().__init__(field_name, comment, date_marked, date_to_do)


class Alter(AbstractChange):
    def __init__(
        self, field_name, date_marked, date_to_do=None, comment=None, *, required
    ):
        if comment is None:
            comment = f'Поле станет {"" if required else "не"}обязательным'
        super().__init__(field_name, comment, date_marked, date_to_do)
        self.required = required


def update_description(meta, fields, own_fields):
    if not hasattr(meta, "changes"):
        return
    for item in meta.changes:
        field = own_fields.get(item.field_name) or deepcopy(fields[item.field_name])
        own_fields[item.field_name] = field
        description = field.kwargs.get("description", "")
        if description:
            description = f". {description}"
        field.kwargs["description"] = f"{item.comment}{description}"
