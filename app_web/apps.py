from django.apps import AppConfig


class AppWebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_web'

    def ready(self):
        import app_web.signals

