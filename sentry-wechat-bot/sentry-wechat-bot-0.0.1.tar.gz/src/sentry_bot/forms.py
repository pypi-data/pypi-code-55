# coding: utf-8

from django import forms


class DingDingOptionsForm(forms.Form):
    send_url = forms.CharField(
        max_length=255,
        help_text='Wechat robot webhook url '
    )
