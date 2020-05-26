from django.shortcuts import render
from django.views.generic import (
                                TemplateView, ListView, FormView,
                                CreateView, UpdateView,
                            )
from django.db.models import Q
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.http import HttpResponseRedirect

from .forms import SearchForm
# Create your views here.


class XListView(ListView, FormView):
    '''
    List view with search and sort criteria
    '''
    template_name = None
    model = None
    queryset = None
    ordering = None
    search_fields = None
    success_url = None
    form_class = SearchForm

    def post(self, request, *args, **kwargs):
        '''
        add keywords to url in post search
        '''
        if request.POST['search']:
            return HttpResponseRedirect("{0}?search={1}".format(
                                                    request.path_info,
                                                    request.POST['search']))
        else:
            return HttpResponseRedirect(request.path_info)

    def get_form_kwargs(self):
        '''
        Return the keyword arguments for instantiating the form.
        '''
        kwargs = super().get_form_kwargs()
        kwargs.update({'search': self.request.GET.get('search')})
        return kwargs

    def get_initial(self):
        '''
        get initial values for the class
        '''
        return {'search': self.request.GET.get('search')}

    def get_context_data(self, *, object_list=None, **kwargs):
        '''
        Get the context for this view.
        '''
        context = super().get_context_data(**kwargs)
        search = None
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
            kwargs.update({'search': search})
        if self.request.GET.get('sort'):
            sort = self.request.GET.get('sort')
            kwargs.update({'sort': sort})
        context.update(kwargs)
        return context

    def get_queryset(self):
        '''
        get queryset
        '''
        queryset = super().get_queryset()
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
        else:
            ordering = ('id', )
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
            fields = dict()
            for field in self.search_fields:
                field += '__contains'
                fields[field] = search
            or_condition = Q()
            for key, value in fields.items():
                or_condition.add(Q(**{key: value}), Q.OR)
            queryset = queryset.filter(
                                or_condition).distinct().order_by(*ordering)
        if self.request.GET.get('sort'):
            sort = self.request.GET.get('sort')
            queryset = queryset.all().order_by(sort)
        return queryset
