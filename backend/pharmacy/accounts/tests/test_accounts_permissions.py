from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from accounts.serializers import CustomUserSerializer


User = get_user_model()

class CustomUserSerializerTestCase(TestCase):
    
    
    def setUp(self):
        self.patient_group = Group.objects.get(name="Patients")
        self.pharmacist_group = Group.objects.get(name="Pharmacists")
        

    def test_create_patient_user_permissions(self):
        patient_data = {
            'username': 'patient_user',
            'password': 'securepassword',
            'role': 'patient',
            'patient_profile': {
                'medical_history': "test"
            }
        }
        serializer = CustomUserSerializer(data=patient_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.role, 'patient')
        self.assertTrue(self.patient_group in user.groups.all())
        self.assertFalse(self.pharmacist_group in user.groups.all())
    

    def test_create_pharmacist_user_permissions(self):
        pharmacist_data = {
            'username': 'pharmacist_user',
            'password': 'securepassword',
            'role': 'pharmacist',
            'pharmacist_profile': {
                'pharmacy_name': 'test',
                'license_number': '1111111'
            }
        }
        serializer = CustomUserSerializer(data=pharmacist_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.role, 'pharmacist')
        self.assertTrue(self.pharmacist_group in user.groups.all())
        self.assertFalse(self.patient_group in user.groups.all())

