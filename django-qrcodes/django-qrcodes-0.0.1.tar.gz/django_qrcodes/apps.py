from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'django_qrcodes'
    label = 'django_qrcodes'
    verbose_name = 'QR Codes'
