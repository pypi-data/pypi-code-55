from django.conf.urls import url
from django.views import generic
from django.urls import include, path

from . import views


urlpatterns = [
    url('^$', generic.RedirectView.as_view(url='./worksheet/'), name="index"),
    url('^activity/', include(views.ActivityModelViewSet().urls)),
    url('^worksheet/', include(views.WorksheetModelViewSet().urls)),
    path('', generic.TemplateView.as_view(template_name="worksheet/index.html"), name="index"),
]