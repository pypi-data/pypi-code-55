from .delete_view import DeleteView


class AdminDeleteView(DeleteView):
    template_name_suffix = "_admin-delete"

