from django.conf import settings as django_settings
from django.test.signals import setting_changed
from django.utils.functional import LazyObject
from django.utils.module_loading import import_string

EVENTS_SETTINGS_NAMESPACE = "HELLWEBPRICE_EVENTS"

class Settings:
    def __init__(self, explicit_overriden_settings: dict = None):
        if explicit_overriden_settings is None:
            explicit_overriden_settings = {}

        overriden_settings = (
            getattr(django_settings, EVENTS_SETTINGS_NAMESPACE, {})
            or explicit_overriden_settings
        )
        self._override_settings(overriden_settings)

    def _override_settings(self, overriden_settings: dict):
        for setting_name, setting_value in overriden_settings.items():
            setattr(self, setting_name, setting_value)

class LazySettings(LazyObject):
    def _setup(self, explicit_overriden_settings=None):
        self._wrapped = Settings(explicit_overriden_settings)

settings = LazySettings()

def reload_django_hellwebprice_events_settings(*args, **kwargs):
    global settings
    setting, value = kwargs['settings'], kwargs['value']
    if setting == EVENTS_SETTINGS_NAMESPACE:
        settings._setup(explicit_overriden_settings=value)

setting_changed.connect(reload_django_hellwebprice_events_settings)