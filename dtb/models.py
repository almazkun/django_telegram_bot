from django.db import models
import uuid
from secrets import token_urlsafe
from dtb.usecases.bot_out import BotOut


def default_secret_token():
    return token_urlsafe(300)[:255]


class ModelBase(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TelegramBot(ModelBase):
    # BOT_TOKEN=1234567890:aaaaaaaaaa_bbbbbbbbbbbbb-cccccccccc
    auth_token = models.CharField(max_length=255)
    # X-Telegram-Bot-Api-Secret-Token
    secret_token = models.CharField(
        max_length=255, default=default_secret_token, editable=False
    )

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("bot_webhook", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.auth_token)

    def set_webhook(self, url):
        return BotOut.set_webhook(url, self.auth_token, self.secret_token)

    def get_webhook_info(self):
        return BotOut.get_webhook_info(self.auth_token)

    def delete_webhook(self):
        return BotOut.set_webhook("", self.auth_token, self.secret_token)


class Chat(ModelBase):
    chat_id = models.CharField(max_length=255)
    bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, related_name="chats")
    chat_info = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.chat_id}"

    def send_message(self, text):
        return BotOut.send_message(self.bot.auth_token, self.chat_id, text)


class Message(ModelBase):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField()
    from_user = models.JSONField(default=dict)
    message_info = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.chat} - {self.text[:10]}..."


class BotCommand(ModelBase):
    bot = models.ForeignKey(
        TelegramBot, on_delete=models.CASCADE, related_name="commands"
    )
    command = models.CharField(max_length=255)
    response = models.TextField()

    def __str__(self):
        return f"{self.command}"
