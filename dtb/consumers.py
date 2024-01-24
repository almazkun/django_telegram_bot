import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from dtb.models import Chat
from dtb.usecases.msg_in import MsgIn

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.chat_pk = self.scope["url_route"]["kwargs"]["pk"]
        self.user = self.scope["user"]

        if not self.user.is_authenticated or not self.user.is_active:
            await self.close()

        try:
            self.chat = await database_sync_to_async(Chat.objects.get)(
                pk=self.chat_pk, bot__created_by=self.user
            )
        except Chat.DoesNotExist:
            await self.close()

        self.group_name = self.chat_pk

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content: dict):
        await database_sync_to_async(MsgIn().accept_websocket_message)(
            self.user, self.chat, content["text"]
        )

    async def chat_message(self, event: dict):
        await self.send_json({"type": "chat_message", **event})

    async def send_chat_message(self, text: str):
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "text": text,
                "sender": self.user.username,
            },
        )
