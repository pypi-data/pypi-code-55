from django import forms
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from web.forms import Form
from web.forms.widgets import TextInput, PasswordInput, CheckboxInput


class LoginForm(Form):
    login_name = forms.CharField(
        max_length=30,
        widget=TextInput(
            attrs={'placeholder': _('Username')}),
        label=_('Username'))
    password = forms.CharField(
        max_length=30,
        widget=PasswordInput(
            attrs={'placeholder': _('Password')}),
        label=_('Password'))
    remember_me = forms.BooleanField(widget=CheckboxInput, label=_('Remember me'), required=False)
    auto_login = forms.BooleanField(widget=CheckboxInput, label=_('Auto login'), required=False)

    def authenticate(self, request):
        login_name = self.cleaned_data['login_name']
        password = self.cleaned_data['password']
        user = authenticate(username=login_name, password=password)
        if user is not None:
            login(request=request, user=user)
        else:
            url = reverse(viewname='muses_login')
            return redirect(to=url)
