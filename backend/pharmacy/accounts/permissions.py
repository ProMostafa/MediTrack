from rest_framework.permissions import BasePermission
from .models import CustomUser, Roles

class IsPatient(BasePermission):
    """
    Allows access only to users with the Patient role.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Roles.PATIRNT

class IsPharmacist(BasePermission):
    """
    Allows access only to users with the Pharmacist role.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Roles.PHARMACIST
