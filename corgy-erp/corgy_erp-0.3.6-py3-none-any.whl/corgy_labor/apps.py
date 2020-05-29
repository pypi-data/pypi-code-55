from django.apps import AppConfig
from material.frontend.apps import ModuleMixin
from django.utils.translation import ugettext_lazy as _

class CorgyLaborConfig(ModuleMixin, AppConfig):
    name = 'corgy_labor'
    verbose_name = _('Labor')
    icon = '<i class="material-icons">settings_applications</i>'
