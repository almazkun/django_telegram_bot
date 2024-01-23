"""This module is used to parse incoming request from telegram bot api and generate response."""

import logging

from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


class BotIn:
    def __init__(self, bot):
        self.bot = bot
        self.bot_from = {
            "id": str(bot.pk),
            "is_bot": True,
            "first_name": bot.name,
        }

    def _is_command(self, text) -> bool:
        return text.startswith("/")

    def _handle_command(self, msg) -> str:
        command = msg.text.split()[0].lower()
        res = self.bot.commands.get(command=command).response
        if "{text}" in res:
            return res.format(text=msg.text)
        elif "{name}" in res:
            return res.format(name=msg.sender)
        return res

    def _handle_message(self, msg):
        res = f"Hello, {msg.sender}! I'm {self.bot_from['first_name']}."
        return msg.chat.messages.create(
            text=res,
            from_user=self.bot_from,
            message_info=msg.message_info,
        ).text

    def _generate_response(self, msg) -> str:
        try:
            if self._is_command(msg.text):
                return self._handle_command(msg)
            return self._handle_message(msg)
        except ObjectDoesNotExist:
            return "Sorry, I don't understand."
        except Exception as e:
            logger.exception(e)
            return "Sorry, something went wrong! Please try again later."

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
        return chat.chat_id, self._generate_response(msg)
