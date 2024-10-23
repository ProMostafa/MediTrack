from django.db import models


class AuditLogActions:
    REGISTER = "registration"
    LOGIN = "login"
    MEDICATION_REQUEST = "medication_request"
    MEDICATION_FULFILLMENT = "medication_fulfillment"


class AuditLog(models.Model):
    ACTION_CHOICES = [
        (AuditLogActions.REGISTER, "User Registration"),
        (AuditLogActions.LOGIN, "User Login"),
        (AuditLogActions.MEDICATION_REQUEST, "Medication Request"),
        (AuditLogActions.MEDICATION_FULFILLMENT, "Medication Fulfillment"),
    ]

    user = models.ForeignKey(
        "accounts.CustomUser", on_delete=models.SET_NULL, null=True
    )
    action = models.CharField(max_length=40, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    details = models.TextField()  # JSON or serialized details can be stored here

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.action}"
    
    @classmethod
    def log(cls, user, action, request, details=None):
        ip_address = cls.get_client_ip(request)
        cls.objects.create(
            user=user,
            action=action,
            ip_address=ip_address,
            details=details
        )

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
