from django.db import models
from ingredients.models import Ingredient
from measurementunits.models import MeasurementUnit  # Adjust the import path as necessary
from recipes.models import Recipe

class RecipeToIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    measurement_unit = models.ForeignKey(MeasurementUnit, on_delete=models.PROTECT)
    quantity = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} of {self.ingredient} in {self.recipe}"

    class Meta:
        ordering = ['recipe']
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gte=0), name='quantity_non_negative')
        ]
