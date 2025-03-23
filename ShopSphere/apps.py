from django.apps import AppConfig


class ShopSphereConfig(AppConfig):
    name = 'ShopSphere'

    def ready(self):
        import ShopSphere.signals 