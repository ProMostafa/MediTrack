from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer
from auditlog.models import AuditLog, AuditLogActions
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed



def health_check(request):
    return JsonResponse({'status': 'healthy'}, status=200)

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        user = None
        details = f"Login attempt for user '{username}'."

        try:
            response = super().post(request, *args, **kwargs)
            user = CustomUser.get_user_by_username(username)
            details = f"User '{username}' logged in successfully."

        except Exception as e:
            response_data = {'detail': str(e)}
            response = Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
            user = None
            details = f"User '{username}' attempt to loging."
            
        AuditLog.log(
            user=user,
            action=AuditLogActions.LOGIN,
            request=request,
            details=details
        )

        return response
