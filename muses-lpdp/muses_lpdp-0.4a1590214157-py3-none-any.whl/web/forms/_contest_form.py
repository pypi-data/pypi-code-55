from db.models import Contest
from web.forms import ModelForm


class ContestForm(ModelForm):
    class Meta:
        model = Contest
        fields = [
            "name",
            "starts_at",
            "ends_at"
        ]
