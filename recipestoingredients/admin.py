# C:\Users\keelim\dev\pantry_pall\recipes\admin.py

from django.contrib import admin
from .models import RecipeToIngredient

@admin.register(RecipeToIngredient)
class RecipeToIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'measurement_unit', 'quantity', 'created_at', 'updated_at')
    search_fields = ('recipe__name', 'ingredient__name', 'measurement_unit__name')
