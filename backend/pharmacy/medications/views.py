from datetime import datetime
from django.utils import timezone
from rest_framework import generics
from accounts.permissions import IsPatient, IsPharmacist
from .models import Medication, Refill
from accounts.models import Roles
from .serializers import MedicationSerializer, RefillSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .utils import get_refill_summary
from auditlog.models import AuditLog, AuditLogActions



class MedicationListView(generics.ListAPIView):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [IsAuthenticated]



class RefillRequestView(generics.ListCreateAPIView):
    serializer_class = RefillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status = self.request.query_params.get("status")
        filters = {}
        if self.request.user.role == Roles.PATIRNT:
            filters = {"user": self.request.user}

        if status:
            filters["status"] = status

        return Refill.objects.filter(**filters)

    def perform_create(self, serializer):
        if not self.request.user.has_perm("medications.can_request_refills"):
            raise PermissionDenied(
                "You do not have permission to create a refill request."
            )
        medication = serializer.validated_data["medication"]
        quantity = serializer.validated_data["quantity"]

        medication.available_quantity -= quantity
        medication.save()
        serializer.save(user=self.request.user)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        AuditLog.log(
            user=self.request.user,
            action=AuditLogActions.MEDICATION_REQUEST,
            request=self.request,
            details=f"Patien {self.request.user} create mediaction request successfully at{current_time}"
        )
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "refill_updates",
            {"type": "refill_status_update", "message": get_refill_summary()},
        )


class CompleteRefillView(APIView):
    permission_classes = [IsAuthenticated, IsPharmacist]

    def post(self, request, pk):
        try:
            if not self.request.user.has_perm("medications.can_approve_refills"):
                raise PermissionDenied(
                    "You do not have permission to create a refill request."
                )
            refill = Refill.objects.get(pk=pk, status="pending")

            refill.status = "completed"
            refill.fulfilled_at = timezone.now()
            refill.fulfilled_by = request.user
            refill.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "refill_updates",
                {"type": "refill_status_update", "message": get_refill_summary()},
            )
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            AuditLog.log(
                user=request.user,
                action=AuditLogActions.MEDICATION_FULFILLMENT,
                request=self.request,
                details=f"Refill_request_no_{refill.id} completed, by pharmacist {request.user} at {current_time}."
            )

            return Response(
                {"detail": "Refill request completed successfully."},
                status=status.HTTP_200_OK,
            )
        except Refill.DoesNotExist:
            return Response(
                {"error": "Refill request not found or already completed."},
                status=status.HTTP_404_NOT_FOUND,
            )


class PharmacistDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsPharmacist]

    def get(self, request):
        dashboard_data = get_refill_summary()
        return Response(dashboard_data)
