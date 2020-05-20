from django.apps import AppConfig
from material.frontend.apps import ModuleMixin
from django.utils.translation import ugettext_lazy as _

class CorgyPayrollConfig(ModuleMixin, AppConfig):
    name = 'corgy_payroll'
    verbose_name = _('Payroll')
    icon = '<i class="material-icons">settings_applications</i>'
