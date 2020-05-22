from django.db import models
from django.utils.translation import ugettext_lazy as _
from viewflow.models import Process
from corgy_mdm import models as mdm_models
# Create your models here.

class PayrollModel(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name = _("Payroll")

class PayrollProcess(Process):
    employee = models.ForeignKey(
        to=mdm_models.EmploymentModel,
        on_delete=models.CASCADE,
        related_name='payrolls',
    )
    approved = models.BooleanField(default=False)
