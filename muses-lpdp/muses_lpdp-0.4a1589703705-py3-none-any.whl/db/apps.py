from django.apps import AppConfig
from django.db.models.signals import post_migrate

from db import init


class DbConfig(AppConfig):
    name = 'db'

    def ready(self):
        post_migrate.connect(init.init, sender=self)
