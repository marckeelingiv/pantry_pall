from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Recipe
from django.contrib.admin.sites import AdminSite
from .admin import RecipeAdmin
from .serializers import RecipeSerializer

User = get_user_model()

class RecipeModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.other_user = get_user_model().objects.create_user(username='otheruser', password='12345')

    def setUp(self):
        self.client = APIClient()
        self.client.login(username='testuser', password='12345')

    def test_create_recipe(self):
        # Test creating a new recipe
        recipe = Recipe.objects.create(
            name='Chocolate Cake',
            description='Delicious dark chocolate cake',
            author=self.user
        )
        self.assertEqual(recipe.name, 'Chocolate Cake')
        self.assertEqual(recipe.description, 'Delicious dark chocolate cake')
        self.assertEqual(recipe.author, self.user)
    
    def test_update_recipe(self):
        recipe = Recipe.objects.create(
            name='Test Recipe',
            description='Test Description',
            author=self.user
        )
        data = {
            'name': 'Updated Recipe',
            'description': 'Updated Description',
            'author': self.user.username
        }
        response = self.client.put(reverse('recipes:recipe-detail', kwargs={'pk': recipe.pk}), data)
        self.assertEqual(response.status_code, 200)
        recipe.refresh_from_db()
        self.assertEqual(recipe.name, 'Updated Recipe')

    def test_delete_recipe(self):
        recipe = Recipe.objects.create(
            name='Test Recipe',
            description='Test Description',
            author=self.user
        )
        response = self.client.delete(reverse('recipes:recipe-detail', kwargs={'pk': recipe.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Recipe.objects.count(), 0)

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

    def test_recipe_admin(self):
        site = AdminSite()
        recipe_admin = RecipeAdmin(Recipe, site)
        self.assertEqual(recipe_admin.list_display, ('name', 'author', 'created_at'))
        self.assertEqual(recipe_admin.search_fields, ('name', 'description'))


    def test_recipe_serializer(self):
        recipe = Recipe.objects.create(
            name='Test Recipe',
            description='Test Description',
            author=self.user
        )
        serializer = RecipeSerializer(recipe)
        self.assertEqual(serializer.data['name'], 'Test Recipe')
        self.assertEqual(serializer.data['description'], 'Test Description')
        self.assertEqual(serializer.data['author'], self.user.username)

    def test_recipe_deserialization(self):
        data = {
            'name': 'Test Recipe',
            'description': 'Test Description',
            'author': self.user.username,
            'created_at': '2023-07-11T00:00:00Z'
        }
        serializer = RecipeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['name'], 'Test Recipe')


    def test_permission_read_only_for_non_author(self):
        # Create a recipe with self.other_user as the author
        recipe = Recipe.objects.create(
            name='Test Recipe',
            description='Test Description',
            author=self.other_user
        )
        
        # Log in as the original user
        self.client.logout()
        self.client.login(username='testuser', password='12345')
        
        # Test that the non-author user can read the recipe
        response = self.client.get(reverse('recipes:recipe-detail', kwargs={'pk': recipe.pk}))
        self.assertEqual(response.status_code, 200)

        # Test that the non-author user cannot update the recipe
        data = {
            'name': 'Updated Recipe'
        }
        response = self.client.put(reverse('recipes:recipe-detail', kwargs={'pk': recipe.pk}), data, format='json')
        self.assertEqual(response.status_code, 403)

        # Test that the non-author user cannot delete the recipe
        response = self.client.delete(reverse('recipes:recipe-detail', kwargs={'pk': recipe.pk}))
        self.assertEqual(response.status_code, 403)

