from db.models import Member
from web.forms import ModelForm


class ThemeSelectorForm(ModelForm):
    class Meta:
        model = Member
        fields = [
            "theme"
        ]
