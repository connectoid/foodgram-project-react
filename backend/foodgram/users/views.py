from django.shortcuts import get_object_or_404, render
from djoser.views import UserViewSet

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.views import APIView


from .serializers import CustomUserSerializer, SubscribeSerializer
from .models import User, Subscribe


class CustomUserViewSet(UserViewSet):
    #lookup_field = 'slug'
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)
    # permission_classes = ([IsAuthenticatedOrReadOnly)
    # pagination_class = LimitOffsetPagination
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # search_fields = ('name',)

    #def get_permissions(self):
    #    if self.action in ('list', 'create'):
    #        permission_classes = (AllowAny,)
    #    else:
    #        permission_classes = (IsAuthenticated,)
    #    return [permission() for permission in permission_classes]

    #@action(detail=False)
    #def me(self, request):
    #    user = request.user
    #    serializer = self.get_serializer(user)
    #    return Response(serializer.data)

class SubscribeViewSet(APIView):
    """
    APIView для добавления и удаления подписки на автора
    """
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]
    #pagination_class = CustomPageNumberPagination

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        if user_id == request.user.id:
            return Response(
                {'error': 'Нельзя подписаться на себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Subscribe.objects.filter(
                user=request.user,
                author_id=user_id
        ).exists():
            return Response(
                {'error': 'Вы уже подписаны на пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author = get_object_or_404(User, id=user_id)
        Subscribe.objects.create(
            user=request.user,
            author_id=user_id
        )
        return Response(
            self.serializer_class(author, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        get_object_or_404(User, id=user_id)
        subscription = Subscribe.objects.filter(
            user=request.user,
            author_id=user_id
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Вы не подписаны на пользователя'},
            status=status.HTTP_400_BAD_REQUEST
        )


class SubscribeListView(ListAPIView):
    """
    APIView для просмотра подписок.
    """
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]
    #pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return User.objects.filter(subscribing__user=self.request.user)