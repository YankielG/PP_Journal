from django.apps import AppConfig


class AppPulseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_pulse'

    def ready(self):
        import app_pulse.signals

