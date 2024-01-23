"""This module performs the use case of creating a bot."""
from django.contrib.auth import get_user_model

from dtb.models import Bot
from dtb.usecases.bot_out import BotOut

START_RESPONSE = """
Hello, {name}!

I am a demo bot. I can help you to get started with Django Telegram Bot.

Try these commands:
    /start - to start the bot
    /help - to get help
    /echo - to echo your message
    /settings - to change settings
"""

HELP_RESPONSE = """
Help:
    /start - to start the bot
    /help - to get help
    /echo - to echo your message
    /settings - to change settings

Check out the source code at https://github.com/almazkun/django_telegram_bot
"""

ECHO_RESPONSE = """
{text}
"""

SETTINGS_RESPONSE = """
There is nothing to change yet.
"""


class BotCreate:
    def __init__(self, auth_token):
        self.bot_out = BotOut(auth_token)

    def _create_bot(self, name=str, auth_token=str, user=get_user_model()) -> Bot:
        return user.bots.create(name=name, auth_token=auth_token)

    def _create_webhook(self, url=str, secret_token=str) -> dict:
        return self.bot_out.set_webhook(url=url, secret_token=secret_token)

    def _create_start_commands(self, bot=Bot) -> None:
        bot.commands.get_or_create(
            command="/start", defaults={"response": START_RESPONSE}
        )
        bot.commands.get_or_create(
            command="/help", defaults={"response": HELP_RESPONSE}
        )
        bot.commands.get_or_create(
            command="/echo", defaults={"response": ECHO_RESPONSE}
        )
        bot.commands.get_or_create(
            command="/settings", defaults={"response": SETTINGS_RESPONSE}
        )

    def perform(self, name=str, auth_token=str, user=get_user_model(), domain=str):
        bot = self._create_bot(name, auth_token, user)
        self._create_webhook(
            url=f"{domain}{bot.get_absolute_url()}", secret_token=bot.secret_token
        )
        self._create_start_commands(bot=bot)
        return bot

    def validate(self):
        try:
            return self.bot_out.get_webhook_info()
        except Exception as e:
            raise e
