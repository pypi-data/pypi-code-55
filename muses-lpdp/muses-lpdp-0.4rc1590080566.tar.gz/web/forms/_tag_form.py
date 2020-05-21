from db.models import Tag
from web.forms import ModelForm


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = [
            "name",
            "enable_at",
            "disable_at",
            "type",
            "mature",
            "active"
        ]
