from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import CustomUser


class RegistrationAPITestCase(APITestCase):

    def setUp(self):
        self.url = reverse("register")

    def test_username_is_required(self):
        payload = {"password": "xxxxxxxxx", "role": "patient", "patient_profile": {}}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"username": ["This field is required."]})

    def test_username_duplicate(self):
        CustomUser.objects.create_user(
            username="patient_user1", password="xxxxxxxxx", role="patient"
        )
        payload = {
            "username": "patient_user1",
            "password": "xxxxxxxxx",
            "role": "patient",
            "patient_profile": {},
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {"username": ["A user with that username already exists."]}
        )

    def test_password_is_required(self):
        payload = {"username": "new_user", "role": "patient", "patient_profile": {}}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"password": ["This field is required."]})

    def test_invalid_role_type(self):
        payload = {
            "username": "new_user",
            "password": "xxxxxxxxx",
            "role": "invalid_role",
            "patient_profile": {},
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"role": ['"invalid_role" is not a valid choice.']})
