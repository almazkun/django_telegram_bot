from django.urls import path

from dtb.consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/chat/<str:pk>/", ChatConsumer.as_asgi(), name="ws_chat"),
]
