from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import CustomUser, Roles
from medications.models import Medication, Refill


class RefillRequestViewTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="patient_user", password="password123"
        )
        self.user.role = Roles.PATIRNT
        self.user.save()
        self.patient_group, created = Group.objects.get_or_create(name="Patients")
        self.user.groups.add(self.patient_group)  # Assign to Pharmacist group

        self.pharmacist_user = CustomUser.objects.create_user(
            username="pharmacist_user", password="password123"
        )
        self.pharmacist_user.role = Roles.PHARMACIST
        self.pharmacist_user.save()
        self.pharmacist_group, created = Group.objects.get_or_create(name="Pharmacists")
        self.pharmacist_user.groups.add(
            self.pharmacist_group
        )  # Assign to Pharmacist group

        self.medication = Medication.objects.create(
            name="Test Medication", available_quantity=10
        )
        self.url = reverse("refill-list-create")

    def get_jwt_token(self, username, password):
        response = self.client.post(
            reverse("login"), {"username": username, "password": password}
        )
        return response.data["access"]

    def test_create_refill_request_success(self):
        token = self.get_jwt_token("patient_user", "password123")
        payload = {
            "medication": self.medication.id,
            "quantity": 5,
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.post(self.url, payload, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Refill.objects.count(), 1)
        refill = Refill.objects.first()
        medication = Medication.objects.first()
        self.assertEqual(refill.medication, self.medication)
        self.assertEqual(refill.quantity, 5)
        self.assertEqual(refill.user, self.user)
        self.assertEqual(medication.available_quantity, 5)

    def test_create_refill_request_permission_denied(self):
        token = self.get_jwt_token("pharmacist_user", "password123")
        payload = {
            "medication": self.medication.id,
            "quantity": 5,
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.post(self.url, payload, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_refill_request_not_enough_stock(self):
        token = self.get_jwt_token("patient_user", "password123")
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "medication": self.medication.id,
            "quantity": 15,
        }
        response = self.client.post(self.url, payload, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "Not enough stock. Available quantity: 10",
        )

    def test_create_refill_request_unauthenticated(self):
        payload = {
            "medication": self.medication.id,
            "quantity": 5,
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
