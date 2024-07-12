from django.urls import reverse
from rest_framework import status
from accounts.models import CustomUser
from rest_framework.test import APITestCase
from django.contrib.auth.tokens import default_token_generator

class RegisterAPITestCase(APITestCase):
    def test_register_success(self):
        data = {
            'name': 'John Doe', 
            'email': 'johndoe@example.com', 
            'password': 'password123'
        }
        response = self.client.post(reverse('signup_user'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Account successfully created, We have sent you a verification email to johndoe@example.com. Click on the link in the email to activate your account.')

class LoginAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='johndoe@example.com', 
            email='johndoe@example.com', 
            password='password123', 
            first_name='John Doe'
        )

    def test_login_success(self):
        data = {'email': 'johndoe@example.com', 'password': 'password123'}
        user = CustomUser.objects.get(email='johndoe@example.com')
        token = default_token_generator.make_token(user)
        verify_data = {'user_id': user.id, 'confirmation_token': token}
        self.client.post(reverse('verify_email'), verify_data, format='json')

        response = self.client.post(reverse('login_user'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid_credentials(self):
        data = {'email': 'johndoe@example.com', 'password': 'wrongpassword'}
        response = self.client.post(reverse('login_user'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Invalid Credentials')

class VerifyEmailAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='johndoe@example.com', 
            email='johndoe@example.com', 
            password='password123', 
            first_name='John Doe'
        )

    def test_verify_email_success(self):
        data = {'user_id': self.user.id, 'confirmation_token': default_token_generator.make_token(self.user)}
        response = self.client.post(reverse('verify_email'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Email Successfully Verified')

    def test_verify_email_invalid_token(self):
        data = {'user_id': self.user.id, 'confirmation_token': 'invalid_token'}
        response = self.client.post(reverse('verify_email'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Token is invalid or expired. Please request another confirmation email.')

class UserRetrieveUpdateAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='johndoe@example.com', email='johndoe@example.com', password='password123', first_name='John Doe')
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_success(self):
        response = self.client.get(reverse('user_account'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'johndoe@example.com')

    def test_update_user_success(self):
        data = {'first_name': 'Jane Doe'}
        response = self.client.patch(reverse('user_account'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Jane Doe')

class ChangePasswordAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='johndoe@example.com', email='johndoe@example.com', password='password123', first_name='John Doe')
        self.client.force_authenticate(user=self.user)

    def test_change_password_success(self):
        data = {'old_password': 'password123', 'new_password': 'newpassword123'}
        response = self.client.patch(reverse('change_password'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Password updated successfully')

    def test_change_password_invalid_old_password(self):
        data = {'old_password': 'wrongpassword', 'new_password': 'newpassword123'}
        response = self.client.patch(reverse('change_password'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Wrong Password')