from django.apps import AppConfig


class ExportappConfig(AppConfig):
    name = 'django_exportapp'

    def ready(self):
        # super().ready()
        self.module.autodiscover_wrapper()
        # debug
        from .helper import exporter
        # print(exporter)
        # for i in exporter.list():
        #     print(i, exporter.arr[i])
