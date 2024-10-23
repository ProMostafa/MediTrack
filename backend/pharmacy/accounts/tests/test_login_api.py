from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import CustomUser

class LoginAPITestCase(APITestCase):

    def setUp(self):
        self.url = reverse('login') 
        self.user = CustomUser.objects.create_user(
            username='test_user',
            password='test_password',
        )
        self.user.role = 'patient'  
        self.user.save()

    def test_login_success(self):
        payload = {
            'username': 'test_user',
            'password': 'test_password',
        }
        response = self.client.post(self.url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['role'], self.user.role)

    def test_login_with_invalid_credentials(self):
        payload = {
            'username': 'wrong_user',
            'password': 'wrong_password',
        }
        response = self.client.post(self.url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('refresh', response.data)
        self.assertNotIn('access', response.data)

    def test_login_without_username(self):
        payload = {
            'password': 'test_password',
        }
        response = self.client.post(self.url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"username": ["This field is required."]})

    def test_login_without_password(self):
        payload = {
            'username': 'test_user',
        }
        response = self.client.post(self.url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"password": ["This field is required."]})
