from django.contrib import admin
from .models import Recipe

class RecipeAdmin(admin.ModelAdmin):
    """
    Custom admin for the Recipe model to enhance admin interface interaction.

    Attributes:
        list_display (tuple): Fields displayed in the list view.
        list_filter (tuple): Fields used for filtering in the admin list.
        search_fields (tuple): Fields searchable in the admin interface.
    """
    list_display = ('name', 'author', 'created_at',)
    list_filter = ('created_at', 'author',)
    search_fields = ('name', 'description',)
    readonly_fields = ('created_at',)

admin.site.register(Recipe, RecipeAdmin)
