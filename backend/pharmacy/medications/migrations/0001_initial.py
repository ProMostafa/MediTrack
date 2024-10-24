# Generated by Django 5.1.2 on 2024-10-22 22:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('available_quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Refill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending', max_length=10)),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('fulfilled_at', models.DateTimeField(blank=True, null=True)),
                ('fulfilled_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pharmacist', to=settings.AUTH_USER_MODEL)),
                ('medication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medications.medication')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('can_request_refills', 'Can request medication refills'), ('can_approve_refills', 'Can approve medication refills'), ('can_view_dashboard', 'Can view dashboard')],
            },
        ),
    ]
