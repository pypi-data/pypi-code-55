from db.models import Admonition
from web.forms import ModelForm


class AdmonitionForm(ModelForm):
    class Meta:
        model = Admonition
        fields = [
            "subject",
            "content"
        ]
