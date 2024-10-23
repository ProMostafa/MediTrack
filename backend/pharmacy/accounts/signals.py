from datetime import datetime
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db.models.signals import post_save
from auditlog.models import AuditLog, AuditLogActions
from .models import PatientProfile, PharmacistProfile


# Signal for PatientProfile
@receiver(post_save, sender=PatientProfile)
def create_patient_profile(sender, instance, created, **kwargs):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if created:
        AuditLog.objects.create(
        user=instance.user,
        action=AuditLogActions.REGISTER,
        details=f'Register patient profile for {instance.user.username} at {current_time}.'
    )

# Signal for PharmacistProfile
@receiver(post_save, sender=PharmacistProfile)
def create_pharmacist_profile(sender, instance, created, **kwargs):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if created:
        AuditLog.objects.create(
        user=instance.user,
        action=AuditLogActions.REGISTER,
        details=f'Register pharmacist profile for {instance.user.username} at {current_time}.'
    )