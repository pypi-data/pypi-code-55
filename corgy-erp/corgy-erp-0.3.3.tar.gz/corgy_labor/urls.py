from django.conf.urls import url
from django.views import generic
from django.urls import include, path

from . import views


urlpatterns = [
    url('^$', generic.RedirectView.as_view(url='./payroll/'), name='index'),
    url('^employee/', include(views.EmploymentModelViewSet().urls)),
    url('^payroll/', include(views.PayrollProcessViewSet().urls)),
    path('', generic.TemplateView.as_view(template_name='corgy_labor/index.html'), name='index'),
]