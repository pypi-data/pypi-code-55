from .create_view import CreateView


class AdminCreateView(CreateView):
    template_name_suffix = "_admin-create"
