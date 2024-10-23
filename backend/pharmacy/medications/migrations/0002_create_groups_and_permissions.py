# Generated by Django 5.1.2 on 2024-10-22 22:47

from django.db import migrations
from django.contrib.contenttypes.models import ContentType
from medications.models import Medication

def create_groups_and_permissions(apps, schema_editor):
    from django.contrib.auth.models import Group, Permission

    # Create groups
    patient_group, created = Group.objects.get_or_create(name='Patients')
    pharmacist_group, created = Group.objects.get_or_create(name='Pharmacists')
    content_type = ContentType.objects.get_for_model(Medication)
    # Define permissions
    can_request_refills, created = Permission.objects.get_or_create(codename='can_request_refills',content_type=content_type)
    can_approve_refills, created = Permission.objects.get_or_create(codename='can_approve_refills',content_type=content_type)
    can_view_dashboard, created = Permission.objects.get_or_create(codename='can_view_dashboard',content_type=content_type)

    # Assign permissions to groups
    patient_group.permissions.add(can_request_refills)
    pharmacist_group.permissions.add(can_approve_refills, can_view_dashboard)


class Migration(migrations.Migration):
    

    dependencies = [
        ('medications', '0001_initial'),
    ]

    operations = [
         migrations.RunPython(create_groups_and_permissions),
    ]
