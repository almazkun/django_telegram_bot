from django.urls import path

from dtb.views import (
    BotCmdCreateView,
    BotCmdDeleteView,
    BotCmdDetailView,
    BotCmdListView,
    BotCmdUpdateView,
    BotCreateView,
    BotDeleteView,
    BotListView,
    BotWebhookView,
    ChatDeleteView,
    ChatDetailView,
    ChatListView,
    MessageListView,
)

urlpatterns = [
    path("api/v1/bot/webhook/<str:pk>/", BotWebhookView.as_view(), name="bot_webhook"),
]

urlpatterns += [
    path(
        "bots/<str:pk>/cmds/create/", BotCmdCreateView.as_view(), name="bot_cmd_create"
    ),
    path("bots/<str:pk>/cmds/", BotCmdListView.as_view(), name="bot_cmd_list"),
    path("bots/<str:pk>/chats/", ChatListView.as_view(), name="chat_list"),
    path("bots/<str:pk>/delete/", BotDeleteView.as_view(), name="bot_delete"),
    path("bots/create/", BotCreateView.as_view(), name="bot_create"),
    path("", BotListView.as_view(), name="bot_list"),
]

urlpatterns += [
    path("chats/<str:pk>/delete/", ChatDeleteView.as_view(), name="chat_delete"),
    path("chats/<str:pk>/", ChatDetailView.as_view(), name="chat_detail"),
]

urlpatterns += [
    path("chats/<str:pk>/messages/", MessageListView.as_view(), name="message_list"),
]

urlpatterns += [
    path("cmds/<str:pk>/update/", BotCmdUpdateView.as_view(), name="bot_cmd_update"),
    path("cmds/<str:pk>/delete/", BotCmdDeleteView.as_view(), name="bot_cmd_delete"),
    path("cmds/<str:pk>/", BotCmdDetailView.as_view(), name="bot_cmd_detail"),
]
