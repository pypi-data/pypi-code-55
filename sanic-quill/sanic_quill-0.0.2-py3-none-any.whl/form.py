from wtforms import (
    Form,
    FormField,
    FileField,
    BooleanField,
    StringField,
    SelectField,
    DecimalField,
    HiddenField,
)
from sanic_quill.fields.wysiwyg import WysiwygField
from sanic_quill.fields.tabs import TabField


LANGUAGE = [
    ('en', u"English")
]


class EditListForm(Form):
    language = HiddenField()
    title = StringField(u"Title")
    content = WysiwygField(u"Content")
    preview = StringField(u"Preview")


class EditForm(Form):
    """Change active on Article methods list"""

    active = BooleanField("Active")
    tabs = TabField(FormField(EditListForm),
                    tabs=LANGUAGE,
                    wysiwyg_fields=['content'],
                    tabs_field='language')
