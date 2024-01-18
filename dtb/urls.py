from django.urls import path

from dtb.views import BotWebhookView


urlpatterns = [
    path("bot/webhook/<str:pk>/", BotWebhookView.as_view(), name="bot_webhook"),
]
