from django.db import models
from django.db.models import BooleanField
from django.db.models import ExpressionWrapper


class BooleanQ(ExpressionWrapper):
    output_field = BooleanField()

    def __init__(self, *args, **kwargs):
        expression = models.Q(*args, **kwargs)
        super().__init__(expression, output_field=None)
