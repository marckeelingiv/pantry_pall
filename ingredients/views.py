from rest_framework import viewsets
from .models import Ingredient
from .serializers import IngredientSerializer
from .permissions import IsAdminOrReadCreateOnly

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOrReadCreateOnly]
