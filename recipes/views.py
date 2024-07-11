from rest_framework import viewsets, filters
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework import permissions
from .permissions import IsAuthorOrReadOnly

class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Recipe instances.
    Handles creating, reading, updating, and deleting operations, applying specific querysets and permissions to requests.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'author__username']

    def get_queryset(self):
        """
        Allow all authenticated users to view all recipes.
        """
        if self.request.user.is_authenticated:
            return Recipe.objects.all()
        return Recipe.objects.none()  # or raise an appropriate permission error

    def perform_create(self, serializer):
        """
        Save the instance of the model with the current user set as the author.
        """
        serializer.save(author=self.request.user)