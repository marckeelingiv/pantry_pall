from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Ingredient

User = get_user_model()

class IngredientTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password123')
        self.normal_user = User.objects.create_user('user', 'user@example.com', 'password123')
        self.ingredient_data = {'name': 'salt', 'description': 'Used in cooking'}
        self.list_create_url = reverse('ingredient-list')

    def test_create_ingredient_as_admin(self):
        self.client.login(username='admin', password='password123')
        response = self.client.post(self.list_create_url, self.ingredient_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

    def test_create_ingredient_as_normal_user(self):
        self.client.login(username='user', password='password123')
        response = self.client.post(self.list_create_url, self.ingredient_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

    def test_create_ingredient_as_unauthenticated_user(self):
        response = self.client.post(self.list_create_url, self.ingredient_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_ingredient_as_admin(self):
        self.client.login(username='admin', password='password123')
        ingredient = Ingredient.objects.create(name='sugar', description='Sweetener')
        url = reverse('ingredient-detail', kwargs={'pk': ingredient.id})
        response = self.client.put(url, {'name': 'sugar', 'description': 'Updated description'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_edit_ingredient_as_normal_user(self):
        self.client.login(username='user', password='password123')
        ingredient = Ingredient.objects.create(name='pepper', description='Spice')
        url = reverse('ingredient-detail', kwargs={'pk': ingredient.id})
        response = self.client.put(url, {'name': 'pepper', 'description': 'Updated description'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    def test_edit_ingredient_as_unauthenticated_user(self):
        ingredient = Ingredient.objects.create(name='garlic', description='Used in cooking')
        url = reverse('ingredient-detail', kwargs={'pk': ingredient.id})
        response = self.client.put(url, {'name': 'garlic', 'description': 'Updated description'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_ingredients_as_authenticated_user(self):
        self.client.login(username='user', password='password123')
        Ingredient.objects.create(name='salt', description='Used in cooking')
        response = self.client.get(self.list_create_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.client.logout()

    def test_list_ingredients_as_unauthenticated_user(self):
        response = self.client.get(self.list_create_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_ingredient_as_admin(self):
        self.client.login(username='admin', password='password123')
        ingredient = Ingredient.objects.create(name='honey', description='Sweetener')
        url = reverse('ingredient-detail', kwargs={'pk': ingredient.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.logout()

    def test_delete_ingredient_as_normal_user(self):
        self.client.login(username='user', password='password123')
        ingredient = Ingredient.objects.create(name='vanilla', description='Flavoring')
        url = reverse('ingredient-detail', kwargs={'pk': ingredient.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    def test_delete_ingredient_as_unauthenticated_user(self):
        ingredient = Ingredient.objects.create(name='basil', description='Herb')
        url = reverse('ingredient-detail', kwargs={'pk': ingredient.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
