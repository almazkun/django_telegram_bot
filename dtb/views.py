from rest_framework.views import APIView
from rest_framework.response import Response
from dtb.usecases.bot_in import BotIn
from dtb.models import TelegramBot, Chat
from dtb.authentication import TelegramBotAuthentication


import logging

logger = logging.getLogger(__name__)


class BotWebhookView(APIView):
    authentication_classes = [TelegramBotAuthentication]

    def post(self, request, *args, **kwargs):
        bot = request.bot
        message = request.data.get("message", None)

        if not message:
            return Response({"status": "ok"})

        chat = Chat.objects.get_or_create(
            chat_id=message["chat"]["id"],
            bot=bot,
            defaults={"chat_info": message["chat"]},
        )[0]
        chat.send_message(BotIn(bot).reply(message))
        return Response({"status": "ok"})
