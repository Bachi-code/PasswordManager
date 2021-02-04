from django.apps import AppConfig


class PasswordsConfig(AppConfig):
    name = 'passwords'

    def ready(self):
        import passwords.signals
