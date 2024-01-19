"""This module is used to make outgoing request to telegram bot api."""

from dtb.providers.telegram import TelegramBotClient


class BotOut:
    client = TelegramBotClient

    def __init__(self, bot):
        self.bot = bot

    def set_webhook(self, url, secret_token):
        return self.client(self.bot.auth_token).set_webhook(url, secret_token)

    def get_webhook_info(self):
        return self.client(self.bot.auth_token).get_webhook_info()

    def send_message(self, chat_id, text):
        return self.client(self.bot.auth_token).send_message(chat_id, text)

    def send_typing(self, chat_id):
        return self.client(self.bot.auth_token).send_typing(chat_id)
