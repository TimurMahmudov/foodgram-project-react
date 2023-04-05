from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Subscription
from .serializers import AuthorOfRecipesSerializer, SubscriptionSerializer


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Вьюсет пользователей"""
    queryset = User.objects.all()

    # Просмотр авторов рецептов, на которых подписан пользователь
    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(subscribe__subscriber=user)
        serializer = AuthorOfRecipesSerializer(queryset,
                                               many=True,
                                               context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Подписка/отписка от авторов рецептов
    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated, )
    )
    def subscribe(self, request, id):
        user, author = request.user, get_object_or_404(User, pk=id)
        author_serializer = AuthorOfRecipesSerializer(
            author, context={'request': request}
        )
        if request.method == 'POST':
            data = {'subscriber': user.id, 'author': id}
            serializer = SubscriptionSerializer(data=data,
                                                context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(author_serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        subscription = get_object_or_404(Subscription,
                                         subscriber=user,
                                         author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
