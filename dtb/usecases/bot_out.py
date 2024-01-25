"""This module is used to make outgoing request to telegram bot api."""

from dtb.providers.telegram import TelegramBotClient


class BotOut:
    client = TelegramBotClient

    def __init__(self, auth_token):
        self.client = self.client(auth_token)

    def get_me(self):
        return self.client.get_me()

    def set_webhook(self, url, secret_token):
        return self.client.set_webhook(url, secret_token)

    def send_message(self, chat_id, text):
        return self.client.send_message(chat_id, text)

    def send_typing(self, chat_id):
        return self.client.send_typing(chat_id)
