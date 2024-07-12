from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Cookbook
from tags.models import Tag

User = get_user_model()

class CookbookTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )
        self.author_user = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='authorpass'
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='regularpass'
        )
        self.tag = Tag.objects.create(
            name='Dessert',
            description='Sweet dishes',
            status='active'
        )
        self.cookbook = Cookbook.objects.create(
            title='Test Cookbook',
            author=self.author_user,
            description='Test description'
        )
        self.cookbook.tags.add(self.tag)
        
        self.client = APIClient()

    def test_list_cookbooks_unauthenticated(self):
        url = reverse('cookbook-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_cookbook_as_author(self):
        self.client.login(username='author', password='authorpass')
        url = reverse('cookbook-list')
        data = {
            'title': 'New Cookbook',
            'author': self.author_user.id,
            'description': 'New description',
            'tags': [self.tag.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_cookbook_as_regular_user(self):
        self.client.login(username='regular', password='regularpass')
        url = reverse('cookbook-list')
        data = {
            'title': 'New Cookbook',
            'author': self.regular_user.id,
            'description': 'New description',
            'tags': [self.tag.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_cookbook_as_author(self):
        self.client.login(username='author', password='authorpass')
        url = reverse('cookbook-detail', args=[self.cookbook.id])
        data = {
            'title': 'Updated Title',
            'author': self.author_user.id,
            'description': 'Updated description',
            'tags': [self.tag.id]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_update_cookbook_as_regular_user(self):
        self.client.login(username='regular', password='regularpass')
        url = reverse('cookbook-detail', args=[self.cookbook.id])
        data = {
            'title': 'Updated Title',
            'description': 'Updated description',
            'tags': [self.tag.id]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_cookbook_as_author(self):
        self.client.login(username='author', password='authorpass')
        url = reverse('cookbook-detail', args=[self.cookbook.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_cookbook_as_regular_user(self):
        self.client.login(username='regular', password='regularpass')
        url = reverse('cookbook-detail', args=[self.cookbook.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_edit_any_cookbook(self):
        self.client.login(username='admin', password='adminpass')
        url = reverse('cookbook-detail', args=[self.cookbook.id])
        data = {
            'title': 'Admin Updated Title',
            'author': self.author_user.id,
            'description': 'Admin updated description',
            'tags': [self.tag.id]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Admin Updated Title')

    def test_admin_can_delete_any_cookbook(self):
        self.client.login(username='admin', password='adminpass')
        url = reverse('cookbook-detail', args=[self.cookbook.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_retrieve_cookbook_detail(self):
        url = reverse('cookbook-detail', args=[self.cookbook.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.cookbook.title)

    def test_filter_cookbooks_by_tags(self):
        url = reverse('cookbook-list')
        response = self.client.get(url, {'tags': self.tag.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.cookbook.title)

    def test_search_cookbooks_by_title(self):
        url = reverse('cookbook-list')
        response = self.client.get(url, {'search': 'Test Cookbook'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.cookbook.title)

    