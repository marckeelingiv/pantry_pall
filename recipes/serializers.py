# C:\Users\keelim\dev\pantry_pall\recipes\serializers.py

from rest_framework import serializers
from .models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Recipe model.

    Maps Recipe instances into JSON format and vice-versa, allowing for easy querying and interaction via API endpoints.
    """
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'author', 'created_at']
