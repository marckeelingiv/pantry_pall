from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a recipe to edit or delete it.
    Any authenticated user can view any recipe.
    """

    def has_permission(self, request, view):
        # Allow any authenticated user to list or view details of recipes
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the author of the recipe
        return obj.author == request.user
