from db.models import Alert
from web.forms import ModelForm


class AlertForm(ModelForm):
    class Meta:
        model = Alert
        fields = [
            "type",
            "details"
        ]
