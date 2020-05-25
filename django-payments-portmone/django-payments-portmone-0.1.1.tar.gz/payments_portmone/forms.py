from django import forms


class PortmoneResponseForm(forms.Form):
    """Response Portmone payment form."""

    APPROVALCODE = forms.CharField(max_length=10)
    SHOPBILLID = forms.CharField(max_length=10)
    SHOPORDERNUMBER = forms.CharField(max_length=256)
    RECEIPT_URL = forms.CharField(max_length=1024)
    RESULT = forms.CharField(max_length=1024)
