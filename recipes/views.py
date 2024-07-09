from rest_framework import viewsets
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission to only allow authors of an object to edit it.
    
    Read permissions are allowed to any request, hence allowing non-destructive requests;
    write permissions are only allowed to the author of the object.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the recipe.
        return obj.author == request.user

class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Recipe instances.

    Handles creating, reading, updating, and deleting operations, applying specific querysets and permissions to requests.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        """Filter the queryset to only include recipes authored by the current authenticated user."""
        return Recipe.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        """Save the instance of the model with the current user set as the author."""
        serializer.save(author=self.request.user)