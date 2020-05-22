from django.apps import AppConfig
from material.frontend.apps import ModuleMixin
from django.utils.translation import ugettext_lazy as _

class CorgyWorksheetConfig(ModuleMixin, AppConfig):
    name = 'corgy_worksheet'
    verbose_name = _('Worksheet')
    icon = '<i class="material-icons">settings_applications</i>'
