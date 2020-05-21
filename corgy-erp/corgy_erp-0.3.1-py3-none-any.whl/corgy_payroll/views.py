from material.frontend.views import ModelViewSet

from . import models


class PayrollModelViewSet(ModelViewSet):
    model = models.PayrollModel
