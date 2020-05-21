from db.models import Message
from web.forms import ModelForm


class MemberForm(ModelForm):
    class Meta:
        model = Message
        fields = [
            "subject",
            "content",
        ]
