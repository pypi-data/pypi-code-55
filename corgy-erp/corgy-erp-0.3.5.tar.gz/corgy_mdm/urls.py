from django.conf.urls import url
from django.views import generic
from django.urls import include, path

from . import views


urlpatterns = [
    url('^$', generic.RedirectView.as_view(url='./person/'), name="index"),
    url('^person/', include(views.PersonModelViewSet().urls)),
    url('^organization/', include(views.OrganizationModelViewSet().urls)),
    path('', generic.TemplateView.as_view(template_name="corgy_mdm/index.html"), name="index"),
]