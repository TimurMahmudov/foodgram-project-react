from rest_framework.routers import SimpleRouter

from .views import CustomUserViewSet

users_router = SimpleRouter()
users_router.register(r'users', CustomUserViewSet, basename='users')
