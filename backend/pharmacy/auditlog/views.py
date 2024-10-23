from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .models import AuditLog

@user_passes_test(lambda u: u.is_staff)
def audit_log_view(request):
    logs = AuditLog.objects.all().order_by('-timestamp')
    return render(request, 'audit_log.html', {'logs': logs})
