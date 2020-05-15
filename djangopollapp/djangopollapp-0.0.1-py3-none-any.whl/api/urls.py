from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from .v1 import urls

urlpatterns = [
    #v1
    path('v1/', include(urls))
]