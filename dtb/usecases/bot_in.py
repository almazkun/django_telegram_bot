"""This module is used to parse incoming request from telegram bot api and generate response."""


class BotIn:
    def __init__(self, bot):
        self.bot = bot

    def reply(self, message) -> str:
        return message
