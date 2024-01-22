"""This module is used to parse incoming request from telegram bot api and generate response."""

import logging

from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


class BotIn:
    def __init__(self, bot):
        self.bot = bot

    def _is_command(self, text):
        return text.startswith("/")

    def _handle_command(self, msg):
        command = msg.text.split()[0].lower()
        res = self.bot.commands.get(command=command).response
        if "{text}" in res:
            return res.format(text=msg.text)
        elif "{name}" in res:
            return res.format(name=msg.sender)
        return res

    def _handle_message(self, msg):
        return ""

    def _generate_response(self, msg) -> str:
        if self._is_command(msg.text):
            return self._handle_command(msg)
        return self._handle_message(msg)

    def reply(self, message) -> str:
        chat_info = message.pop("chat", {})
        text = message.pop("text", "")
        from_user = message.pop("from", {})

        chat = self.bot.chats.get_or_create(
            chat_id=chat_info.get("id"),
            defaults={"chat_info": chat_info},
        )[0]
        msg = chat.messages.create(
            text=text,
            from_user=from_user,
            message_info=message,
        )
        try:
            return chat.chat_id, self._generate_response(msg)
        except ObjectDoesNotExist:
            return f"Sorry, `{text}` command is not found."
        except Exception as e:
            logger.exception(e)
            return chat.chat_id, "Sorry, something went wrong! Please try again later."
