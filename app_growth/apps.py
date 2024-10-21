from django.apps import AppConfig


class AppGrowthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_growth'

    def ready(self):
        import app_growth.signals

