from django.apps import AppConfig


class AppPressureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_pressure'

    def ready(self):
        import app_pressure.signals

