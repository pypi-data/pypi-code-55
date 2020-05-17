from .list_view import ListView


class AdminListView(ListView):
    template_name_suffix = "_admin-list"
    paginate_by = 10

