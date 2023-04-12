from api.v1.router_v1 import router_v1
from django.urls import include, path

urlpatterns = [
    path('', include(router_v1.urls)),
]
