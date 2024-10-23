from django.urls import path
from .views import MedicationListView, RefillRequestView, CompleteRefillView, PharmacistDashboardView

urlpatterns = [
    path('', MedicationListView.as_view(), name='medication-list'),
    path('refills/', RefillRequestView.as_view(), name='refill-list-create'),
    path('refills/complete/<int:pk>/', CompleteRefillView.as_view(), name='complete-refill'),
    path('dashboard/', PharmacistDashboardView.as_view(), name='pharmacist-dashboard'),
    
]