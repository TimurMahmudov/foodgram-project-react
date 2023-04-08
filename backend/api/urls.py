from django.urls import include, path

from api.v1.router_v1 import router_v1


urlpatterns = [
    path('', include(router_v1.urls)),
]
