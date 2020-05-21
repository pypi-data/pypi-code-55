from .list_view import ListView


class ModListView(ListView):
    template_name_suffix = "_mod-list"
    paginate_by = 10
