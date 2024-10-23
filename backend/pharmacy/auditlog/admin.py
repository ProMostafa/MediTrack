# admin.py

from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp','ip_address', 'details')
    search_fields = ('user__username', 'action', 'details')
    list_filter = ('action', 'timestamp')
    ordering = ('-timestamp',)
