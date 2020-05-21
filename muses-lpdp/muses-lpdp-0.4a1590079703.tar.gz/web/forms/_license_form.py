from db.models import License
from web.forms import ModelForm


class LicenseForm(ModelForm):
    class Meta:
        model = License
        fields = [
            "name"
        ]
