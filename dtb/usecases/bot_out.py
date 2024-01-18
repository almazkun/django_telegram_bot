"""This module is used to make outgoing request to telegram bot api."""

from dtb.providers.telegram import TelegramBotClient


class BotOut:
    client = TelegramBotClient

    @classmethod
    def set_webhook(cls, url, auth_token, secret_token):
        return cls.client(auth_token).set_webhook(url, secret_token)

    @classmethod
    def get_webhook_info(cls, auth_token):
        return cls.client(auth_token).get_webhook_info()

    @classmethod
    def send_message(cls, auth_token, chat_id, text):
        return cls.client(auth_token).send_message(chat_id, text)
