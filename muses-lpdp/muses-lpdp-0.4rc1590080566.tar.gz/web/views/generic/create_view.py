from django.http import Http404
from django.utils.decorators import classonlymethod
from django.views.generic import CreateView as CV


class CreateView(CV):
    template_name_suffix = "_create"
    section_name = ""

    @classonlymethod
    def as_view(cls, **initkwargs):
        if initkwargs.get("model"):
            cls.model = initkwargs.get("model")
        return super().as_view(**initkwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get("model"):
            self.model = kwargs.get("model")
        self.section_title = kwargs.get("section_title", None)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        identifier = self.kwargs.get("id")
        if identifier is not None:
            queryset = queryset.filter(id=identifier)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj
