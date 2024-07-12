from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import CustomUser
from django.contrib.auth.tokens import default_token_generator

class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('signup_user')

    def test_register_user(self):
        data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().email, 'testuser@example.com')

    def test_register_user_with_existing_email(self):
        CustomUser.objects.create_user(
            username='testuser@example.com', 
            email='testuser@example.com', 
            password='testpassword', 
            first_name='Test User')
        data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 1)

class UserLoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login_user')
        self.user = CustomUser.objects.create_user(
            username='testuser@example.com', 
            email='testuser@example.com', 
            password='testpassword', 
            first_name='Test User', 
            is_verify=True)

    def test_login_user(self):
        # Verify user is correctly saved and is_verify is True
        user = CustomUser.objects.get(email='testuser@example.com')
        self.assertTrue(self.user.is_verify)
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_unverified_user(self):
        self.user.is_verify = False
        self.user.save()
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class EmailVerificationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.verify_url = reverse('verfiy_email')
        self.user = CustomUser.objects.create_user(
            username='testuser@example.com', 
            email='testuser@example.com', 
            password='testpassword', 
            first_name='Test User'
        )
        self.token = default_token_generator.make_token(self.user)

    def test_verify_email(self):
        data = {
            'user_id': self.user.id,
            'confirmation_token': self.token
        }
        response = self.client.post(self.verify_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verify)

    def test_verify_email_with_invalid_token(self):
        data = {
            'user_id': self.user.id,
            'confirmation_token': 'invalidtoken'
        }
        response = self.client.post(self.verify_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_verify)

class UserProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='testuser@example.com', 
            email='testuser@example.com', 
            password='testpassword', 
            first_name='Test User', 
            is_verify=True
        )
        self.client.force_authenticate(user=self.user)
        self.profile_url = reverse('user_account')

    def test_retrieve_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_profile(self):
        data = {
            'first_name': 'Updated Name'
        }
        response = self.client.put(self.profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated Name')

