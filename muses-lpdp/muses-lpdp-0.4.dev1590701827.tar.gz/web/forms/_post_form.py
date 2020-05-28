from db.models import Post
from web.forms import ModelForm


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "summary",
            "content"
        ]
