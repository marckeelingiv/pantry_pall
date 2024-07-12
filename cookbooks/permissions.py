# permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow authors of a cookbook to edit or delete it.
    Assumes the Cookbook model has an `author` attribute.
    """

    def has_permission(self, request, view):
        # Allow read-only access for any request
        if request.method in SAFE_METHODS:
            return True
        # Allow authenticated users to create cookbooks
        if request.method == 'POST' and request.user.is_authenticated:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in SAFE_METHODS:
            return True
        # Admin users can edit or delete any cookbook
        if request.user.is_staff:
            return True
        # Write permissions are only allowed to the author of the cookbook
        return obj.author == request.user
