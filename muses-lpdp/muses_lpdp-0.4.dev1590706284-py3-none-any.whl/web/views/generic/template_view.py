from django.views.generic import TemplateView as TV


class TemplateView(TV):
    section_name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.section_title = kwargs.get("section_title", None)
