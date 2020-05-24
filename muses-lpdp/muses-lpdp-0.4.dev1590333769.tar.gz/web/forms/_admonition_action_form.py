from db.models import AdmonitionAction
from web.forms import ModelForm


class AdmonitionActionForm(ModelForm):
    class Meta:
        model = AdmonitionAction
        fields = [
            "message",
        ]
