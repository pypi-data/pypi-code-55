from db.models import Book
from web.forms import ModelForm


class AlertForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "isbn",
            "published_at",
            "author",
            "license",
            "visible"
        ]
