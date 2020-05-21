from db.models import CorrectionRequest
from web.forms import ModelForm


class CorrectionRequestForm(ModelForm):
    class Meta:
        model = CorrectionRequest
        fields = [
            "created_at"
            "title",
        ]
