from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "sarscov2"
    verbose_name = "SARS-COV-2"
    include_in_administration_section = True
    has_exportable_data = True
