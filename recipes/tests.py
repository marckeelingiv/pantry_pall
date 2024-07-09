from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Recipe

class RecipeModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = get_user_model().objects.create_user(username='testuser', password='12345')

    def test_recipe_creation(self):
        # Test creating a new recipe
        recipe = Recipe.objects.create(
            name='Chocolate Cake',
            description='Delicious dark chocolate cake',
            author=self.user
        )
        self.assertEqual(recipe.name, 'Chocolate Cake')
        self.assertEqual(recipe.description, 'Delicious dark chocolate cake')
        self.assertEqual(recipe.author, self.user)

    def test_string_representation(self):
        # Test the string representation of the Recipe model
        recipe = Recipe(
            name='Vanilla Ice Cream',
            author=self.user
        )
        self.assertEqual(str(recipe), 'Vanilla Ice Cream')

    def test_cascade_delete(self):
        # Test that deleting a user also deletes their recipes
        recipe = Recipe.objects.create(name='Banana Bread', author=self.user)
        self.assertEqual(Recipe.objects.count(), 1)
        self.user.delete()
        self.assertEqual(Recipe.objects.count(), 0)
