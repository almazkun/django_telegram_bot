from typing import Any

from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from dtb.authentication import BotAuthentication, LoginReqMix
from dtb.forms import BotCreateForm, LoginForm, SignUpForm
from dtb.models import Bot, BotCommand, Chat
from dtb.usecases.bot_out import BotOut
from dtb.usecases.msg_in import MsgIn


class BotWebhookView(APIView):
    authentication_classes = [BotAuthentication]

    def post(self, request, *args, **kwargs):
        bot = request.bot
        message = request.data.get("message", None)

        if not message:
            return Response({"status": "ok"})

        BotOut(bot.auth_token).send_typing(message["chat"]["id"])
        msg_in = MsgIn()
        msg_in.accept_telegram_message(bot, message)
        msg_in.generate_response()
        return Response({"status": "ok"})


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "dtb/signup.html"
    success_url = reverse_lazy("login")


class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = "dtb/login.html"
    success_url = reverse_lazy("bot_list")


class MyLogoutView(LoginReqMix, LogoutView):
    def get_success_url(self):
        return reverse_lazy("bot_list")


class BotListCreateView(LoginReqMix, ListView, FormView):
    model = Bot
    template_name = "dtb/bot_list.html"
    context_object_name = "bot_list"
    form_class = BotCreateForm
    success_url = reverse_lazy("bot_list")

    def form_valid(self, form):
        form.user = self.request.user
        form.domain = settings.DEMO_DOMAIN
        form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.bots.all()

    def get_template_names(self) -> list[str]:
        if self.request.htmx:
            return ["dtb/includes/bot_list.html"]
        return super().get_template_names()


class BotDetailView(LoginReqMix, DetailView):
    model = Bot
    template_name = "dtb/bot_detail.html"
    context_object_name = "bot"

    def get_queryset(self) -> QuerySet[Any]:
        return self.request.user.bots.all().prefetch_related("commands")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["command_list"] = self.object.commands.all()
        return context


class BotDeleteView(LoginReqMix, DeleteView):
    model = Bot
    success_url = reverse_lazy("bot_list")


class ChatListView(LoginReqMix, DetailView):
    model = Bot
    template_name = "dtb/chat_list.html"
    context_object_name = "bot"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chat_list"] = self.object.chats.all()
        return context


class ChatDeleteView(LoginReqMix, DeleteView):
    model = Chat
    success_url = reverse_lazy("chat_list")


class MessageListView(LoginReqMix, DetailView):
    model = Chat
    template_name = "dtb/chat_list.html"
    context_object_name = "chat_selected"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chat_list"] = self.object.bot.chats.all()
        context["message_list"] = self.object.messages.all()
        return context


class BotCmdListView(LoginReqMix, ListView):
    model = BotCommand
    template_name = "dtb/bot_cmd_list.html"
    context_object_name = "bot_cmds"


class BotCmdCreateView(LoginReqMix, CreateView):
    model = BotCommand
    fields = ["command", "response"]
    template_name = "dtb/bot_cmd_create.html"
    success_url = reverse_lazy("bot_cmd_list")


class BotCmdDetailView(LoginReqMix, DetailView):
    model = BotCommand
    template_name = "dtb/bot_cmd_detail.html"
    context_object_name = "bot_cmd"


class BotCmdUpdateView(LoginReqMix, UpdateView):
    model = BotCommand
    fields = ["command", "response"]
    template_name = "dtb/bot_cmd_update.html"
    success_url = reverse_lazy("bot_cmd_list")


class BotCmdDeleteView(LoginReqMix, DeleteView):
    model = BotCommand
    success_url = reverse_lazy("bot_cmd_list")
