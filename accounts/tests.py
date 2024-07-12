from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import CustomUser
from django.contrib.auth.tokens import default_token_generator


class UserRegistrationTests(APITestCase):

    def test_user_can_register(self):
        url = reverse('signup_user')
        data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().email, 'testuser@example.com')

class EmailVerificationTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='testpassword123',
            first_name='Test'
        )
        self.user.is_verify = False
        self.user.save()

    def test_email_verification(self):
        url = reverse('verfiy_email')
        confirmation_token = default_token_generator.make_token(self.user)
        data = {
            'user_id': self.user.id,
            'confirmation_token': confirmation_token
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verify)

class UserLoginTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='testpassword123',
            first_name='Test',
            is_verify=True
        )

    def test_login_after_verification(self):
        url = reverse('login_user')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class PasswordChangeTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='testpassword123',
            first_name='Test',
            is_verify=True
        )
        self.client.force_authenticate(user=self.user)

    def test_change_password(self):
        url = reverse('change_password')
        data = {
            'old_password': 'testpassword123',
            'new_password': 'newtestpassword123'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newtestpassword123'))

class ProfileUpdateTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User',
            is_verify=True
        )
        self.admin_user = CustomUser.objects.create_superuser(
            username='adminuser@example.com',
            email='adminuser@example.com',
            password='adminpassword123',
            first_name='Admin',
            last_name='User'
        )
        self.client.force_authenticate(user=self.user)

    def test_user_can_update_own_profile(self):
        url = reverse('user_account')
        data = {
            'first_name': 'UpdatedTest',
            'last_name': 'UpdatedUser'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'UpdatedTest')
        self.assertEqual(self.user.last_name, 'UpdatedUser')

    def test_non_admin_cannot_update_others_profile(self):
        url = reverse('user_account')
        data = {
            'first_name': 'UpdatedTest',
            'last_name': 'UpdatedUser'
        }
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_others_profile(self):
        url = reverse('user_account')
        data = {
            'first_name': 'UpdatedTest',
            'last_name': 'UpdatedUser'
        }
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class InvalidLoginTests(APITestCase):

    def test_invalid_login(self):
        url = reverse('login_user')
        data = {
            'email': 'nonexistentuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Invalid Credentials')

class UnauthorizedProfileAccessTests(APITestCase):
    def test_unauthorized_access(self):
        url = reverse('user_account')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
