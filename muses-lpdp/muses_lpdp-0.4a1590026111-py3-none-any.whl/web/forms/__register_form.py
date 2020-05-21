from django import forms
from django.utils.translation import gettext_lazy as _

from web.forms import Form
from web.forms.widgets import TextInput, PasswordInput, SelectDateWidget, EmailInput, CheckboxInput


class RegisterForm(Form):
    login_name = forms.CharField(
        max_length=30,
        widget=TextInput(
            attrs={'placeholder': _('Username')}),
        label=_('Username'))
    email = forms.EmailField(
        max_length=100,
        widget=EmailInput(
            attrs={'placeholder': _('Email')}),
        label=_('Email'))
    password = forms.CharField(
        max_length=30,
        widget=PasswordInput(
            attrs={'placeholder': _('Password')}),
        label=_('Password'))
    passwordRepeat = forms.CharField(
        max_length=30,
        widget=PasswordInput(
            attrs={'placeholder': _('Repeat your password')}),
        label=_('Repeat your password'))
    birth_date = forms.DateField(
        widget=SelectDateWidget(
            attrs={'placeholder': _('Birth date')}),
        label=_('Birth date'))
    cgu_accept = forms.BooleanField(
        required=True,
        widget=CheckboxInput(),
        label=_('I have read and accept the CGU')
    )

    def register(self):
        pass
