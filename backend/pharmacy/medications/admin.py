from django.contrib import admin
from .models import Medication, Refill

# Register your models here.
@admin.register(Medication)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "available_quantity"]
    
@admin.register(Refill)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["user", "medication", "quantity", "status", "requested_at", "fulfilled_at"]
    
