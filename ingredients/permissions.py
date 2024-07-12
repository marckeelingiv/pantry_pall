from rest_framework import permissions

class IsAdminOrReadCreateOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit ingredients.
    Any authenticated user can create ingredients.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff
