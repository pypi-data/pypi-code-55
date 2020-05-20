from django.apps import AppConfig
from material.frontend.apps import ModuleMixin
from django.utils.translation import ugettext_lazy as _

class CorgyMdmConfig(ModuleMixin, AppConfig):
    name = 'corgy_mdm'
    verbose_name = _('Master data')
    icon = '<i class="material-icons">settings_applications</i>'
