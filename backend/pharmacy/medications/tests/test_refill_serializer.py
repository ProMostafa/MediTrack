from rest_framework.test import APITestCase
from accounts.models import CustomUser
from medications.serializers import RefillSerializer
from medications.models import Refill, Medication, RefillStatus

class RefillSerializerTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test_user', password='test_password')
        self.medication = Medication.objects.create(name='Test Medication', available_quantity=10)
        self.refill = Refill.objects.create(
            medication=self.medication,
            quantity=5,
            user=self.user,
            status=RefillStatus.PENDING
        )
        
        self.serializer = RefillSerializer(instance=self.refill)


    def test_validate_available_quantity_success(self):
        data = {
            'medication': self.medication.id,
            'quantity': 5,
        }
        serializer = RefillSerializer(data=data, context={'request': self.user})
        serializer.is_valid()
        print(serializer.errors)
        self.assertTrue(serializer.is_valid())

    def test_validate_available_quantity_failure(self):
        # Invalid quantity (greater than available)
        data = {
            'medication': self.medication.id,
            'quantity': 15,
        }
        serializer = RefillSerializer(data=data, context={'request': self.user})
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual(serializer.errors['non_field_errors'][0], "Not enough stock. Available quantity: 10")

    def test_validate_quantity_zero(self):
        # Invalid quantity (zero)
        data = {
            'medication': self.medication.id,
            'quantity': 0,
        }
        serializer = RefillSerializer(data=data, context={'request': self.user})
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual(serializer.errors['non_field_errors'][0],"Quantity should be greater than or equal 1")
