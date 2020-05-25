from django.conf.urls import url
from django.views import generic
from django.urls import include, path

from . import views


urlpatterns = [
    url('^$', generic.RedirectView.as_view(url='./accountmodel/'), name="index"),
    url('^accountmodel/', include(views.AccountModelViewSet().urls)),
    path('', generic.TemplateView.as_view(template_name="corgy_accounts/index.html"), name="index"),
]