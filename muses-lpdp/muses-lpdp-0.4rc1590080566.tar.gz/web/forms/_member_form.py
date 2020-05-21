from db.models import Member
from web.forms import ModelForm


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "is_active"
        ]
