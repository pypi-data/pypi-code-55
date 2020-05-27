from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class CapitalistAccountValidator:
    message = _('Invalid Capitalist account number.')
    code = 'invalid_capitalist_account'
    account_types = (
        'R',  # rub
        'U',  # usd
        'E',  # eur
        'T',  # usd tether
        'B',  # btc
    )

    def __init__(self, account_types=None):
        self.account_types = account_types

    def __call__(self, value):
        if len(value) < 2 or value[0] not in self.account_types:
            raise ValidationError(self.message, code=self.code)
        try:
            int(value[1:])
        except ValueError:
            raise ValidationError(self.message, code=self.code)
