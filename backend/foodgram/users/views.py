from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Subscribe, User
from .serializers import CustomUserSerializer, SubscribeSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)


class SubscribeViewSet(APIView):
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        if user_id == request.user.id:
            return Response(
                {'errors': 'Нельзя подписаться на себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Subscribe.objects.filter(
                user=request.user,
                author_id=user_id
        ).exists():
            return Response(
                {'errors': 'Вы уже подписаны на пользователя'},
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
        if subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Вы не подписаны на пользователя'},
            status=status.HTTP_400_BAD_REQUEST
        )


class SubscribeListView(ListAPIView):
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(subscribing__user=self.request.user)
