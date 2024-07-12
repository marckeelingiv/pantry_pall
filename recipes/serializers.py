# C:\Users\keelim\dev\pantry_pall\recipes\serializers.py

from rest_framework import serializers
from .models import Recipe
from django.contrib.auth import get_user_model

User = get_user_model()

class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Recipe model.

    Maps Recipe instances into JSON format and vice-versa, allowing for easy querying and interaction via API endpoints.
    """
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'author', 'created_at']
