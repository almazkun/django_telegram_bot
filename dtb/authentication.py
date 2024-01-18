from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from dtb.models import TelegramBot


class TelegramBotAuthentication(BaseAuthentication):
    """This to check request from telegram bot,
    to make sure that they have `X-Telegram-Bot-Api-Secret-Token` header
    and it is valid.
    And populate `request.bot` with the bot object.
    """

    def authenticate(self, request):
        secret_token = request.META.get("HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN", None)
        if not secret_token:
            raise AuthenticationFailed("Missing X-Telegram-Bot-Api-Secret-Token")
        try:
            bot = TelegramBot.objects.get(
                pk=request.parser_context["kwargs"]["pk"], secret_token=secret_token
            )
            request.bot = bot
        except TelegramBot.DoesNotExist:
            raise AuthenticationFailed("Invalid X-Telegram-Bot-Api-Secret-Token")
        return (bot, None)
