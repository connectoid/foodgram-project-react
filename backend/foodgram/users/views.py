from django.shortcuts import get_object_or_404, render
from djoser.views import UserViewSet

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import CustomUserSerializer
from .models import User


class CustomUserViewSet(UserViewSet):
    #lookup_field = 'slug'
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)
    # permission_classes = ([IsAuthenticatedOrReadOnly)
    # pagination_class = LimitOffsetPagination
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # search_fields = ('name',)

    def get_permissions(self):
        if self.action in ('list', 'create'):
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

