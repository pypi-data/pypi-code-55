#!/usr/bin/python

from importlib import import_module


def autoload_module(value):
    from django.apps import apps
    for app_config in apps.get_app_configs():
        # print(app_config)
        try:
            import_module('%s.%s' % (app_config.name, value))
        except Exception:
            pass
