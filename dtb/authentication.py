import logging

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from dtb.models import Bot

logger = logging.getLogger(__name__)


class BotAuthentication(BaseAuthentication):
    """This to check request from Telegram,
    to make sure that they have `X-Telegram-Bot-Api-Secret-Token` header
    and it is valid.
    And populate `request.bot` with the bot object.
    """

    auth_header = "HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN"
    miss_log = "BotAuthentication.authenticate: Missing %s from %s for bot %s"
    invalid_log = "BotAuthentication.authenticate: Invalid %s: %s from %s for bot %s"

    def authenticate(self, request):
        secret_token = request.META.get(self.auth_header, None)
        if not secret_token:
            logger.warning(
                self.miss_log,
                self.auth_header,
                request.META.get("REMOTE_ADDR", ""),
                request.parser_context["kwargs"]["pk"],
            )
            raise AuthenticationFailed("Missing " + self.auth_header)
        try:
            bot = Bot.objects.get(
                pk=request.parser_context["kwargs"]["pk"], secret_token=secret_token
            )
            request.bot = bot
        except Bot.DoesNotExist:
            logger.warning(
                self.invalid_log,
                self.auth_header,
                secret_token,
                request.META.get("REMOTE_ADDR", ""),
                request.parser_context["kwargs"]["pk"],
            )
            raise AuthenticationFailed("Invalid " + self.auth_header)
        return (bot, None)
