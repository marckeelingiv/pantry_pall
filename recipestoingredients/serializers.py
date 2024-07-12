# C:\Users\keelim\dev\pantry_pall\recipes\serializers.py

from rest_framework import serializers
from .models import RecipeToIngredient

class RecipeToIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeToIngredient
        fields = '__all__'
