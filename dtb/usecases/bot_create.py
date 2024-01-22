"""This module performs the use case of creating a bot."""
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
    def __init__(self, domain, bot_name, bot_token, user):
        self.domain = domain
        self.bot_name = bot_name
        self.bot_token = bot_token
        self.user = user
        self.bot = None

    def _create_bot(self):
        if not self.bot:
            self.bot = self.user.bots.get_or_create(
                name=self.bot_name, auth_token=self.bot_token
            )[0]
        return self.bot

    def _create_webhook(self):
        return (
            BotOut(self.bot)
            .set_webhook(
                f"{self.domain}{self.bot.get_absolute_url()}", self.bot.secret_token
            )
            .result()
        )

    def _create_start_command(self):
        self.bot.commands.get_or_create(
            command="/start", defaults={"response": START_RESPONSE}
        )
        self.bot.commands.get_or_create(
            command="/help", defaults={"response": HELP_RESPONSE}
        )
        self.bot.commands.get_or_create(
            command="/echo", defaults={"response": ECHO_RESPONSE}
        )
        self.bot.commands.get_or_create(
            command="/settings", defaults={"response": SETTINGS_RESPONSE}
        )

    def perform(self):
        self._create_bot()
        self._create_webhook()
        self._create_start_command()
        return self.bot
