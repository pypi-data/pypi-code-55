from django.apps import AppConfig


class Covid19Config(AppConfig):
    name = 'covid19'
    verbose_name = '新冠肺炎疫情'

    def ready(self):
        import covid19.signals