from django.forms import Widget


class TagsSelectInput(Widget):
    def __init__(self, attrs=None):
        super().__init__(attrs)

    class Media:
        css: {
        }
        js: {

        }
