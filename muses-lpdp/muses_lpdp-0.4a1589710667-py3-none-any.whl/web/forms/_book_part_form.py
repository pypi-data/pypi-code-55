from db.models import BookPart
from web.forms import ModelForm


class BookPartForm(ModelForm):
    class Meta:
        model = BookPart
        fields = [
            "title",
            "order",
            "book"
        ]
