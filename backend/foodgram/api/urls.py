from django.urls import include, path
from rest_framework import routers

from .views import TagViewSet

router = routers.SimpleRouter()

router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    #path('v1/auth/signup/', confirmation_code, name='signup'),
    #path('v1/auth/token/', get_jwt_token, name='token'),
    path('v1/', include(router.urls)),
]