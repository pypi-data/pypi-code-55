from django.shortcuts import render
from material.frontend.views import ModelViewSet
from . import models

# Create your views here.


class WorksheetModelViewSet(ModelViewSet):
    model = models.WorksheetModel


class ActivityModelViewSet(ModelViewSet):
    model = models.ActivityModel
