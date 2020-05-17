from db.models import AdmonitionTemplate
from web.forms import ModelForm


class AdmonitionTemplateForm(ModelForm):
    class Meta:
        model = AdmonitionTemplate
        fields = [
            "subject",
            "content"
        ]
