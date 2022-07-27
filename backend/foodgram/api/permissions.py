from rest_framework import permissions

class OwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        bool = request.method in permissions.SAFE_METHODS or request.user.is_authenticated
        print('has permission', bool)
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
            )

    def has_object_permission(self, request, view, obj):
        bool = obj.author == request.user
        print('has object permission', bool)
        return obj.author == request.user

class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS