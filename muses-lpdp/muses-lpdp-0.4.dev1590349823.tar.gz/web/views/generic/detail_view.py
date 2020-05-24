from django.http import Http404
from django.utils.decorators import classonlymethod
from django.views.generic import DetailView as DV
from django.utils.translation import gettext as _


class DetailView(DV):
    template_name_suffix = "_detail"
    section_name = ""

    @classonlymethod
    def as_view(cls, **initkwargs):
        if initkwargs.get("model"):
            cls.model = initkwargs.get("model")
        return super().as_view(**initkwargs)

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
