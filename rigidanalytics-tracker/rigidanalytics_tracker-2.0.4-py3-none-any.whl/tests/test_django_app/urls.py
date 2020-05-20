# from django.urls import path
from django.conf.urls import url

from tests.test_django_app import views


urlpatterns = [
    url('', views.home),
]
