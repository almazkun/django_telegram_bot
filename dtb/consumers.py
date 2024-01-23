from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from dtb.models import Chat, Message


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.chat_pk = self.scope["url_route"]["kwargs"]["pk"]
        self.user = self.scope["user"]

        if not self.user.is_authenticated or not self.user.is_active:
            await self.close()

        chat_exists = await database_sync_to_async(
            Chat.objects.filter(pk=self.chat_pk, users=self.user).exists
        )()

        if not chat_exists:
            await self.close()

        self.group_name = self.chat_pk

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.send_system_notification(f"{self.user.username} has joined the chat")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.send_system_notification(f"{self.user.username} has left the chat")

    async def receive_json(self, content, **kwargs):
        msg = await Message.objects.acreate(
            sender=self.user, text=content["message"], chat_id=self.chat_pk
        )
        await self.channel_layer.group_send(
            self.group_name,
            {
                "sender": msg.sender.username,
                "message": msg.text,
                "type": "chat_message",
            },
        )

    async def chat_message(self, event):
        await self.send_json({"type": "chat_message", **event})

    async def system_notification(self, event):
        await self.send_json({"type": "system_notification", **event})

    async def send_system_notification(self, message):
        await self.channel_layer.group_send(
            self.group_name,
            {"type": "system_notification", "message": message, "sender": "system"},
        )
