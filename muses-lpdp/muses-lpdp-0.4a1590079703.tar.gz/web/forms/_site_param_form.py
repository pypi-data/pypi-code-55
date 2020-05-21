from db.models import SiteParam
from web.forms import ModelForm
from web.forms.widgets import TextInput


class SiteParamForm(ModelForm):
    class Meta:
        model = SiteParam
        fields = [
            "key",
            "value",
        ]
        widgets = {
            'key': TextInput(),
            'value': TextInput(),
        }
