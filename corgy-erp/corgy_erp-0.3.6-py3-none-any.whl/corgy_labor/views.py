from material.frontend.views import ModelViewSet

from . import models

class EmploymentModelViewSet(ModelViewSet):
    model = models.EmploymentModel

class PayrollProcessViewSet(ModelViewSet):
    model = models.PayrollProcess

