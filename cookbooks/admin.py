from django.contrib import admin
from .models import Cookbook

@admin.register(Cookbook)
class CookbookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('author', 'tags')
