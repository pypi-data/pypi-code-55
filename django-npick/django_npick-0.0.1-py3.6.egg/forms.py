from django import forms

from .models import Icon
from .widgets import IconWidget


class IconForm(forms.ModelForm):
    name = forms.CharField(widget=IconWidget)

    class Meta:
        model = Icon
        fields = ['name']

