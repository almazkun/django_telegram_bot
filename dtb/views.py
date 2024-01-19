import logging

from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from dtb.authentication import BotAuthentication
from dtb.models import Bot, BotCommand, Chat
from dtb.usecases.bot_in import BotIn
from dtb.usecases.bot_out import BotOut

logger = logging.getLogger(__name__)


class BotWebhookView(APIView):
    authentication_classes = [BotAuthentication]

    def post(self, request, *args, **kwargs):
        bot = request.bot
        message = request.data.get("message", None)

        if not message:
            return Response({"status": "ok"})

        bot_out = BotOut(bot)
        bot_out.send_typing(message["chat"]["id"])
        chat_id, response = BotIn(bot).reply(message)
        bot_out.send_message(chat_id, response)
        return Response({"status": "ok"})


class BotListView(ListView):
    model = Bot
    template_name = "dtb/bot_list.html"
    context_object_name = "bots"


class BotCreateView(CreateView):
    model = Bot
    fields = ["name", "auth_token"]
    template_name = "dtb/bot_create.html"
    success_url = reverse_lazy("bot_list")


class BotDeleteView(DeleteView):
    model = Bot
    success_url = reverse_lazy("bot_list")


class ChatListView(DetailView):
    model = Bot
    template_name = "dtb/chat_list.html"
    context_object_name = "bot"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chats"] = self.object.chats.all()
        return context


class ChatDetailView(DetailView):
    model = Chat
    template_name = "dtb/chat_detail.html"
    context_object_name = "chat"


class ChatDeleteView(DeleteView):
    model = Chat
    success_url = reverse_lazy("chat_list")


class MessageListView(DetailView):
    model = Chat
    template_name = "dtb/message_list.html"
    context_object_name = "chat"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messages"] = self.object.messages.all()
        return context


class BotCmdListView(ListView):
    model = BotCommand
    template_name = "dtb/bot_cmd_list.html"
    context_object_name = "bot_cmds"


class BotCmdCreateView(CreateView):
    model = BotCommand
    fields = ["command", "response"]
    template_name = "dtb/bot_cmd_create.html"
    success_url = reverse_lazy("bot_cmd_list")


class BotCmdDetailView(DetailView):
    model = BotCommand
    template_name = "dtb/bot_cmd_detail.html"
    context_object_name = "bot_cmd"


class BotCmdUpdateView(UpdateView):
    model = BotCommand
    fields = ["command", "response"]
    template_name = "dtb/bot_cmd_update.html"
    success_url = reverse_lazy("bot_cmd_list")


class BotCmdDeleteView(DeleteView):
    model = BotCommand
    success_url = reverse_lazy("bot_cmd_list")
