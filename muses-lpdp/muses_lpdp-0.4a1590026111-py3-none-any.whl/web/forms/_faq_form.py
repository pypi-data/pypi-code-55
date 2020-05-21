from db.models import Faq
from web.forms import ModelForm


class FaqForm(ModelForm):
    class Meta:
        model = Faq
        fields = [
            "question",
            "answer",
        ]
