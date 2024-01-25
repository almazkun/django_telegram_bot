import logging
from abc import ABC, abstractmethod

from django.core.exceptions import ObjectDoesNotExist

from dtb.cacher import ActiveUserCache
from dtb.models import Bot, Chat, CustomUser, Message
from dtb.types import TelegramMessage
from dtb.usecases.msg_out import MsgOut

logger = logging.getLogger(__name__)


class Provider(ABC):
    @abstractmethod
    def save(self, incoming_message: dict):
        pass

    @abstractmethod
    def response_to(self, message: Message):
        pass


class TelegramProvider(Provider):
    def save(self, incoming_message: dict):
        self.bot = incoming_message["bot"]
        msg = incoming_message["msg"].copy()
        chat_info = msg.pop("chat", {})
        text = msg.pop("text", "")
        from_user = msg.pop("from", {})

        self.chat = self.bot.chats.get_or_create(
            chat_id=chat_info.get("id"),
            defaults={"chat_info": chat_info},
        )[0]
        return self.chat.messages.create(
            text=text,
            from_user=from_user,
            message_info=msg,
        )

    def response_to(self, message: Message):
        res = self._generate_response(message)
        if res:
            return self.chat.messages.create(
                text=res,
                from_user={
                    "id": str(self.bot.pk),
                    "is_bot": True,
                    "first_name": self.bot.name,
                },
            )

    def _is_command(self, text) -> bool:
        return text.startswith("/")

    def _handle_command(self, message: Message) -> str:
        command = message.text.split()[0].lower()
        res = self.bot.commands.get(command=command).response
        if "{text}" in res:
            return res.format(text=message.text)
        elif "{name}" in res:
            return res.format(name=message.sender)
        return res

    def _handle_message(self, message: Message) -> str:
        active_admins = ActiveUserCache(str(self.chat.pk)).get()
        if not active_admins:
            return "Sorry, no admins are currently online. You may find help at /start."

    def _generate_response(self, message: Message) -> str:
        try:
            if self._is_command(message.text):
                return self._handle_command(message)
            return self._handle_message(message)
        except ObjectDoesNotExist:
            return "Sorry, I don't understand."
        except Exception as e:
            logger.exception(e)
            return "Sorry, something went wrong! Please try again later."


class WebsocketProvider(Provider):
    def save(self, incoming_message: dict):
        return Message.objects.create(
            text=incoming_message["text"],
            chat=incoming_message["chat"],
            from_user={
                "id": str(incoming_message["user"].pk),
                "is_bot": False,
                "first_name": incoming_message["user"].first_name,
                "last_name": incoming_message["user"].last_name,
                "username": incoming_message["user"].username,
            },
        )

    def response_to(self, message: Message):
        # We do not generate response for websocket messages
        # We only send the message to the listening clients
        return message


class MsgIn:
    def __init__(self):
        self.message = None
        self.provider = None
        self.response = None

    def accept_telegram_message(self, bot: Bot, msg: TelegramMessage):
        self.incoming_message = {"provider": "telegram", "bot": bot, "msg": msg}

    def accept_websocket_message(self, user: CustomUser, chat: Chat, text: str):
        self.incoming_message = {
            "provider": "websocket",
            "user": user,
            "chat": chat,
            "text": text,
        }

    def save_message(self):
        self.provider = (
            TelegramProvider()
            if self.incoming_message["provider"] == "telegram"
            else WebsocketProvider()
        )
        self.message = self.provider.save(self.incoming_message)

    def create_response(self):
        self.response = self.provider.response_to(self.message)

    def generate_response(self):
        self.save_message()
        self.create_response()
        if isinstance(self.provider, TelegramProvider):
            MsgOut.send_message_to_ws(self.message)
        MsgOut.send_message(self.response)
