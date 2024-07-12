# C:\Users\keelim\dev\pantry_pall\recipes\tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Recipe, Ingredient, MeasurementUnit, RecipeToIngredient
from django.contrib.auth import get_user_model

User = get_user_model()

class RecipeToIngredientModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            description='Test Description',
            author=self.user
        )
        self.ingredient = Ingredient.objects.create(name='Test Ingredient')
        self.measurement_unit = MeasurementUnit.objects.create(name='Test Unit')

    def test_recipe_to_ingredient_creation(self):
        recipe_to_ingredient = RecipeToIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            measurement_unit=self.measurement_unit,
            quantity=1.0
        )
        self.assertEqual(recipe_to_ingredient.recipe, self.recipe)
        self.assertEqual(recipe_to_ingredient.ingredient, self.ingredient)
        self.assertEqual(recipe_to_ingredient.measurement_unit, self.measurement_unit)
        self.assertEqual(recipe_to_ingredient.quantity, 1.0)

    def test_quantity_non_negative(self):
        with self.assertRaises(Exception):
            RecipeToIngredient.objects.create(
                recipe=self.recipe,
                ingredient=self.ingredient,
                measurement_unit=self.measurement_unit,
                quantity=-1.0
            )


class RecipeToIngredientAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            description='Test Description',
            author=self.user
        )
        self.ingredient = Ingredient.objects.create(name='Test Ingredient')
        self.measurement_unit = MeasurementUnit.objects.create(name='Test Unit')

        self.recipe_to_ingredient = RecipeToIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            measurement_unit=self.measurement_unit,
            quantity=1.0
        )

    def test_list_recipe_to_ingredients(self):
        url = reverse('recipe-to-ingredient-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_recipe_to_ingredient(self):
        url = reverse('recipe-to-ingredient-list')
        data = {
            'recipe': self.recipe.id,
            'ingredient': self.ingredient.id,
            'measurement_unit': self.measurement_unit.id,
            'quantity': 2.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RecipeToIngredient.objects.count(), 2)

    def test_retrieve_recipe_to_ingredient(self):
        url = reverse('recipe-to-ingredient-detail', args=[self.recipe_to_ingredient.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_recipe_to_ingredient(self):
        url = reverse('recipe-to-ingredient-detail', args=[self.recipe_to_ingredient.id])
        data = {
            'recipe': self.recipe.id,
            'ingredient': self.ingredient.id,
            'measurement_unit': self.measurement_unit.id,
            'quantity': 3.0
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.recipe_to_ingredient.refresh_from_db()
        self.assertEqual(self.recipe_to_ingredient.quantity, 3.0)

    def test_delete_recipe_to_ingredient(self):
        url = reverse('recipe-to-ingredient-detail', args=[self.recipe_to_ingredient.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RecipeToIngredient.objects.count(), 0)
