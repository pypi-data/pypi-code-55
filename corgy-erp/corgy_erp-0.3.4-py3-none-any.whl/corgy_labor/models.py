from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from viewflow.models import Process
from corgy_mdm import models as mdm_models
# Create your models here.


class EmploymentModel(models.Model):

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')

    person = models.ForeignKey(
        verbose_name=_('person'),
        to=mdm_models.PersonModel,
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )

    organization = models.ForeignKey(
        verbose_name=_('organization'),
        to=mdm_models.OrganizationModel,
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )

    begin = models.DateTimeField(
        verbose_name=_('begin'),
        default=timezone.now,
        blank=False,
        null=False
    )

    end = models.DateTimeField(
        verbose_name=_('end'),
        default=None,
        blank = True,
        null = True,
    )

class LaborStatementProcess(Process):

    class Meta:
        verbose_name = _('labor statement'),
        verbose_name_plural = _('labor statements'),

    employer = models.ForeignKey(
        verbose_name = _('employer'),
        to=mdm_models.OrganizationModel,
        on_delete=models.CASCADE,
        related_name='employer_labor_statement_processes',
    )

    employee = models.ForeignKey(
        verbose_name=_('employee'),
        to=mdm_models.PersonModel,
        on_delete=models.CASCADE,
        related_name='employee_labor_statement_processes',
    )

    laborer = models.ForeignKey(
        to=EmploymentModel,
        on_delete=models.CASCADE,
        related_name='labor_statement_processes',
    )

    approved = models.BooleanField(default=False)

class PayrollProcess(Process):

    class Meta:
        verbose_name = _('payroll'),
        verbose_name_plural = _('payrolls'),

    employee = models.ForeignKey(
        to=EmploymentModel,
        on_delete=models.CASCADE,
        related_name='payrolls',
    )
    approved = models.BooleanField(default=False)
