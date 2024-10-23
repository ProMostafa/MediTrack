from django.db import models

from accounts.models import CustomUser, PharmacistProfile

class RefillStatus:
    PENDING = 'pending'
    COMPLETE = 'complete'
    
# Create your models here.
class Medication(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    available_quantity = models.IntegerField()


    def __str__(self):
        return self.name


class Refill(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    requested_at = models.DateTimeField(auto_now_add=True)
    fulfilled_at = models.DateTimeField(null=True, blank=True)
    fulfilled_by = models.ForeignKey(
        CustomUser,
        related_name="pharmacist",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    
    class Meta:
        permissions = [
            ("can_request_refills", "Can request medication refills"),
            ("can_approve_refills", "Can approve medication refills"),
            ("can_view_dashboard", "Can view dashboard"),
        ]

    def __str__(self):
        return f"{self.medication.name} - {self.user.username} ({self.status})"
