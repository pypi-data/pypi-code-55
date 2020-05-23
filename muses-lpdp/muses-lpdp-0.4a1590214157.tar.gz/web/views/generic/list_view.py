from django.views.generic import ListView as LV


class ListView(LV):
    template_name_suffix = "_list"
    paginate_by = 10
    section_name = ""


