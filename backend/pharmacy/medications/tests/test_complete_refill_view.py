from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from accounts.models import CustomUser, Roles
from unittest.mock import patch, AsyncMock
from medications.models import Medication, Refill

class CompleteRefillViewTestCase(APITestCase):

    def setUp(self):
        self.pharmacist_group, _ = Group.objects.get_or_create(name='Pharmacists')

        self.pharmacist_user = CustomUser.objects.create_user(username='pharmacist_user', password='password123', role=Roles.PHARMACIST)
        self.pharmacist_user.groups.add(self.pharmacist_group)

        self.patient_user = CustomUser.objects.create_user(username='patient_user', password='password123', role=Roles.PATIRNT)

        self.medication = Medication.objects.create(name='Test Medication', available_quantity=10)

        self.refill_request = Refill.objects.create(
            medication=self.medication,
            quantity=5,
            status='pending',
            user=self.patient_user,
        )

        self.url = reverse('complete-refill', args=[self.refill_request.pk])

    def get_jwt_token(self, username, password):
        response = self.client.post(reverse('login'), {'username': username, 'password': password})
        return response.data['access']

    def test_complete_refill_success(self):
        token = self.get_jwt_token('pharmacist_user', 'password123')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = self.client.post(self.url, headers=headers)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.refill_request.refresh_from_db()
        self.assertEqual(self.refill_request.status, "completed")
        self.assertIsNotNone(self.refill_request.fulfilled_at)
        self.assertEqual(self.refill_request.fulfilled_by, self.pharmacist_user)


    @patch('medications.views.get_channel_layer')  # Mock the channel layer if needed
    def test_complete_refill_not_found(self, new_callable=AsyncMock):
        token = self.get_jwt_token('pharmacist_user', 'password123')

        non_existing_url = reverse('complete-refill', args=[999])
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = self.client.post(non_existing_url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Refill request not found or already completed.", response.data['error'])

    @patch('medications.views.get_channel_layer')
    def test_complete_refill_without_permission(self, new_callable=AsyncMock):
        token = self.get_jwt_token('patient_user', 'password123')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = self.client.post(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("You do not have permission to perform this action.", response.data['detail'])
