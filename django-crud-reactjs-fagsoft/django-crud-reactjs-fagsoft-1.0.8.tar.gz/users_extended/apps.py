from django.apps import AppConfig


class UsersExtendedConfig(AppConfig):
    name = 'users_extended'

    def ready(self):
        import users_extended.signals
