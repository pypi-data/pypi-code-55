from django.apps import AppConfig
from material.frontend.apps import ModuleMixin
from django.utils.translation import ugettext_lazy as _

class CorgyAccountsConfig(ModuleMixin, AppConfig):
    name = 'corgy_accounts'
    verbose_name = _('Accounts')
    icon = '<i class="material-icons">settings_applications</i>'