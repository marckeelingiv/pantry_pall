# C:\Users\keelim\dev\pantry_pall\recipes\urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeToIngredientViewSet

router = DefaultRouter()
router.register(r'recipe-to-ingredient', RecipeToIngredientViewSet, basename='recipetoingredient')

urlpatterns = [
    path('', include(router.urls)),
]
