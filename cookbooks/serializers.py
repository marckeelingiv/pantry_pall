from rest_framework import serializers
from .models import Cookbook

class CookbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cookbook
        fields = '__all__'
