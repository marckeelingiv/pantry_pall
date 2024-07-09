from rest_framework import viewsets
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the recipe.
        return obj.author == request.user

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        # Only return recipes for the current authenticated user
        return Recipe.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        # Assign the recipe's author to the current user
        serializer.save(author=self.request.user)