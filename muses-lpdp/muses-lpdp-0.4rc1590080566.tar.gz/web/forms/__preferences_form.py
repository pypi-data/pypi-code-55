import pytz
from django import forms
from django.utils.translation import gettext_lazy as _

from web.forms import MultiForm
from web.forms.widgets import CheckboxInput


class PreferencesNotificationsForm(MultiForm):
    email_notification_on_new_comment = forms.BooleanField(
        widget=CheckboxInput, label=_('email notification on new comment'), required=False
    )
    email_notification_on_new_message = forms.BooleanField(
        widget=CheckboxInput, label=_('email notification on new message'), required=False
    )

    def save_notification_settings(self):
        pass


class PreferencesGeneralForm(MultiForm):
    ALL_TIMEZONES = sorted((item, item) for item in pytz.all_timezones)
    tz_name = forms.ChoiceField(choices=ALL_TIMEZONES)
