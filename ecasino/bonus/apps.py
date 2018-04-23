from django.apps import AppConfig


class BonusConfig(AppConfig):
    name = 'bonus'

    def ready(self):
        from . import signals
