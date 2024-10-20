from django.apps import AppConfig


class AppWeightConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_weight'

    def ready(self):
        import app_weight.signals

