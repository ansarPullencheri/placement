from django.contrib import admin

# Register your models here.
from django.apps import AppConfig

class WebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web'

    def ready(self):
        import web.signals  # Connect signals

