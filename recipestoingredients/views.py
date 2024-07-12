# C:\Users\keelim\dev\pantry_pall\recipes\views.py

from rest_framework import viewsets
from .models import RecipeToIngredient
from .serializers import RecipeToIngredientSerializer

class RecipeToIngredientViewSet(viewsets.ModelViewSet):
    queryset = RecipeToIngredient.objects.all()
    serializer_class = RecipeToIngredientSerializer
