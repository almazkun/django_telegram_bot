from django.urls import path

from dtb.views import (
    BotCmdCreateView,
    BotCmdDeleteView,
    BotCmdDetailView,
    BotCmdListView,
    BotCmdUpdateView,
    BotDeleteView,
    BotDetailView,
    BotListCreateView,
    BotWebhookView,
    ChatDeleteView,
    ChatListView,
    MessageListView,
    MyLoginView,
    MyLogoutView,
    PredictorUpdateView,
    SignUpView,
)

urlpatterns = [
    path("accounts/login/", MyLoginView.as_view(), name="login"),
    path("accounts/logout/", MyLogoutView.as_view(), name="logout"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
]

urlpatterns += [
    path("api/v1/bot/webhook/<str:pk>/", BotWebhookView.as_view(), name="bot_webhook"),
]

urlpatterns += [
    path(
        "bots/<str:pk>/cmds/create/", BotCmdCreateView.as_view(), name="bot_cmd_create"
    ),
    path("bots/<str:pk>/cmds/", BotCmdListView.as_view(), name="bot_cmd_list"),
    path("bots/<str:pk>/chats/", ChatListView.as_view(), name="chat_list"),
    path("bots/<str:pk>/delete/", BotDeleteView.as_view(), name="bot_delete"),
    path(
        "bots/<str:pk>/predictor/update/",
        PredictorUpdateView.as_view(),
        name="predictor_update",
    ),
    path("bots/<str:pk>/", BotDetailView.as_view(), name="bot_detail"),
    path("", BotListCreateView.as_view(), name="bot_list"),
]

urlpatterns += [
    path("chats/<str:pk>/delete/", ChatDeleteView.as_view(), name="chat_delete"),
]

urlpatterns += [
    path("chats/<str:pk>/messages/", MessageListView.as_view(), name="message_list"),
]

urlpatterns += [
    path("cmds/<str:pk>/update/", BotCmdUpdateView.as_view(), name="bot_cmd_update"),
    path("cmds/<str:pk>/delete/", BotCmdDeleteView.as_view(), name="bot_cmd_delete"),
    path("cmds/<str:pk>/", BotCmdDetailView.as_view(), name="bot_cmd_detail"),
]
