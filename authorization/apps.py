from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'authorization'

    def ready(self):
        import authorization.signals
