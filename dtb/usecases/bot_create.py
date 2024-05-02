"""This module performs the use case of creating a bot."""

import logging

from django.contrib.auth import get_user_model

from dtb.models import Bot
from dtb.usecases.bot_out import BotOut

logger = logging.getLogger(__name__)

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


class AuthTokenValidationError(Exception):
    pass


class BotCreate:
    def __init__(self, auth_token):
        self.auth_token = auth_token
        self.bot_out = BotOut(auth_token)
        self.name_ = None

    def _get_me(self):
        try:
            self.name_ = self.bot_out.get_me().result().get("result").get("first_name")
            return self.name_
        except Exception as e:
            logger.exception(e)
            raise e

    @property
    def name(self):
        if not self.name_:
            self._get_me()
        return self.name_

    def _create_bot(self, user=get_user_model()) -> Bot:
        return user.bots.create(name=self.name, auth_token=self.auth_token)

    def _create_webhook(self, bot=Bot, domain=str) -> dict:
        return self.bot_out.set_webhook(
            url=f"{domain}{bot.get_absolute_url()}", secret_token=bot.secret_token
        )

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

    def perform(self, user=get_user_model(), domain=str):
        bot = self._create_bot(user)
        self._create_webhook(bot, domain)
        self._create_start_commands(bot=bot)
        return bot

    def validate(self):
        return self._get_me()
