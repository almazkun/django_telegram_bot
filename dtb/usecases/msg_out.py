from abc import ABC, abstractmethod

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from dtb.models import Message
from dtb.types import WsTypes
from dtb.usecases.bot_out import BotOut


async def send_message_to_chat(group_name: str, text: str, sender: str, type_: WsTypes):
    """This function sends a received Telegram message to a Websocket group"""
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        group_name,
        {
            "type": type_,
            "text": text,
            "sender": sender,
        },
    )


class Listener(ABC):
    @abstractmethod
    def send(self, msg):
        pass


class TelegramListener(Listener):
    def send(self, msg):
        BotOut(msg.chat.bot.auth_token).send_message(msg.chat.chat_id, msg.text)


class WebsocketListener(Listener):
    def send(self, msg):
        async_to_sync(send_message_to_chat)(
            str(msg.chat.pk),
            msg.text,
            msg.sender,
            "chat_message",
        )


class MsgOut:
    """This should accept send message to all listening clients"""

    @classmethod
    def send_message(cls, message: Message):
        cls.send_message_to_ws(message)
        cls.send_message_to_telegram(message)

    @classmethod
    def send_message_to_ws(cls, message: Message):
        if message:
            WebsocketListener().send(message)

    @classmethod
    def send_message_to_telegram(cls, message: Message):
        if message:
            TelegramListener().send(message)
