from db.models import Comment
from web.forms import ModelForm


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content"
        ]
