# from django.conf import settings

from .utils import autoload_module

__all__ = []


def autodiscover_wrapper():
    # print(dir(settings))
    # if settings.EXPORTAPP_ENABLE is True:
    autoload_module('_exportapp')


default_app_config = 'django_exportapp.apps.ExportappConfig'
