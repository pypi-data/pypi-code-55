from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class PayrollModel(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name = _("Payroll")