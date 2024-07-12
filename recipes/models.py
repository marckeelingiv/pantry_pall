from django.db import models
from django.conf import settings

class Recipe(models.Model):
    """
    Recipe model storing details about recipes authored by users.

    Attributes:
        name (CharField): Name of the recipe.
        description (TextField): Description of the recipe.
        author (ForeignKey): Reference to the user who authored the recipe, related to Django's user model.
        created_at (DateTimeField): The timestamp when the recipe was created, automatically set to the current datetime.
    """
    name = models.CharField(max_length=255, verbose_name="Recipe Name")
    description = models.TextField(verbose_name="Recipe Description")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Author")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name_plural = "Recipes"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
