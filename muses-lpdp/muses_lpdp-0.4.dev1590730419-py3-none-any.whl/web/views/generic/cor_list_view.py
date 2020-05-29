from .list_view import ListView


class CorListView(ListView):
    template_name_suffix = "_cor-list"
    paginate_by = 10
