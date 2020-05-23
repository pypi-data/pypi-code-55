from django import forms
from django.utils.translation import gettext_lazy as _

from web.forms import MultiForm
from web.forms.widgets import TextInput, SelectDateWidget


class ProfileGeneralInformationForm(MultiForm):
    username = forms.CharField(
        max_length=30,
        widget=TextInput(
            attrs={'placeholder': _('Username')}),
        label=_('Username'))

    birth_date = forms.DateField(
        widget=SelectDateWidget(
            attrs={'placeholder': _('Birth date')}),
        label=_('Birth date'))

    def save_general_information(self):
        pass
