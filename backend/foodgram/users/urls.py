from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, SubscribeListView, SubscribeViewSet

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path(
        'users/subscriptions/',
        SubscribeListView.as_view(),
        name='subscriptions'
    ),
    path(
        'users/<int:user_id>/subscribe/',
        SubscribeViewSet.as_view(),
        name='subscribe'
    ),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]