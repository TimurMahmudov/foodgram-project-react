from rest_framework import routers


class NewDefaultRouter(routers.DefaultRouter):
    """Основной роутер"""
    def extend(self, router):
        self.registry.extend(router.registry)
