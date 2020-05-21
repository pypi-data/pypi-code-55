from django.shortcuts import render
from material.frontend.views import ModelViewSet

from . import models

# Create your views here.


class PersonModelViewSet(ModelViewSet):
    model = models.PersonModel
