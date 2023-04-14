from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from users.models import Subscription

from .mixins import CreateDestroyObjView
from .users_serializers import (AuthorOfRecipesSerializer,
                                SubscriptionSerializer)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """
    Вьюсет пользователей
    """
    def get_queryset(self):
        return User.objects.order_by('username')

    """
    Просмотр авторов рецептов, на которых подписан пользователь
    """
    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(
            subscribe__user=user
        ).order_by('username')
        set_in_pages = self.paginate_queryset(queryset=queryset)
        serializer = AuthorOfRecipesSerializer(set_in_pages,
                                               many=True,
                                               context={'request': request})
        return self.get_paginated_response(serializer.data)


class CreateDestroySubscribeViewSet(CreateDestroyObjView):
    """
    Подписка/отписка от авторов рецептов
    """
    serializer_class = SubscriptionSerializer
    model_obj = User
    model_connection = Subscription
    response_serializer = AuthorOfRecipesSerializer

    def get_queryset(self):
        return self.request.user.subscriber

    def create(self, request, user_id):
        return super().create(request, user_id)

    def destroy(self, request, user_id):
        return super().destroy(request, user_id)
