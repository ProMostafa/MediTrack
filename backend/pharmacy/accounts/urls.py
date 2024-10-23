from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, health_check
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("health/", health_check),  # Add the health check endpoint
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
