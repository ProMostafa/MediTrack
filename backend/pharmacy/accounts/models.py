
from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


from enum import Enum



from auditlog.models import AuditLog

class Roles:
    PATIRNT = "patient"
    PHARMACIST = "pharmacist"

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        (Roles.PATIRNT, 'Patient'),
        (Roles.PHARMACIST, 'Pharmacist'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    
    
    @classmethod
    def get_user_by_username(cls, username):
        return cls.objects.filter(username=username).first()
    

class PatientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    medical_history = models.TextField(blank=True, null=True)
    
    # Add other patient-specific fields

class PharmacistProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    pharmacy_name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=255)
    # Add other pharmacist-specific fields
    
    
    
