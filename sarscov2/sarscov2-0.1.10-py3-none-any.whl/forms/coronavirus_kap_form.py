from django import forms
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from ..models import CoronavirusKap
from .coronavirus_kap_form_validator import CoronaKapFormValidator


class CoronavirusKapForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = CoronaKapFormValidator

    screening_identifier = forms.CharField(
        label="Subject Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = CoronavirusKap
        fields = "__all__"
