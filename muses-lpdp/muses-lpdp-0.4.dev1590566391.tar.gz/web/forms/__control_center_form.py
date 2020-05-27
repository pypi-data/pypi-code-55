from django import forms
from django.utils.translation import gettext_lazy as _

from web.forms import MultiForm
from web.forms.widgets import PasswordInput, EmailInput


class ControlCenterChangePasswordForm(MultiForm):
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

    def change_password(self):
        pass


class ControlCenterChangeEmailForm(MultiForm):
    email = forms.EmailField(
        max_length=100,
        widget=EmailInput(
            attrs={'placeholder': _('Email')}),
        label=_('Email'))
    emailRepeat = forms.EmailField(
        max_length=100,
        widget=EmailInput(
            attrs={'placeholder': _('Repeat your email')}),
        label=_('Repeat your email'))

    def change_email(self):
        pass
