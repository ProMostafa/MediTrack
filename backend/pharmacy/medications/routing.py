from django.urls import path
from .consumers import RefillConsumer

websocket_urlpatterns = [
    path('ws/refills/', RefillConsumer.as_asgi()),
]
