# C:\Users\keelim\dev\pantry_pall\recipes\serializers.py

from rest_framework import serializers
from .models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'author', 'created_at']
