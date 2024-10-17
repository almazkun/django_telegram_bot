import re
import uuid
from secrets import token_urlsafe

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import truncatechars
from django.urls import reverse


def default_secret_token():
    return token_urlsafe(200)[:255]


def validate_command(value):
    if not re.match(r"^/[a-zA-Z0-9_]{1,32}$", value):
        raise ValidationError(
            "Command should start with /, contain up to 32 of Latin letters, numbers and underscores"
        )


class RoleChoices(models.IntegerChoices):
    SYSTEM = (0, "system")
    ASSISTANT = (1, "assistant")
    USER = (2, "user")


class CustomUser(AbstractUser):
    objects = UserManager()

    managed_bots = models.ManyToManyField("Bot", related_name="managers", blank=True)


class ModelBase(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Bot(ModelBase):
    name = models.CharField(
        max_length=32,
        help_text="Human-readable name for thr reference",
    )
    auto_response = models.BooleanField(default=False)
    # BOT_TOKEN=1234567890:aaaaaaaaaa_bbbbbbbbbbbbb-cccccccccc
    auth_token = models.CharField(
        max_length=255, unique=True, help_text="You can get it from BotFather"
    )
    # X-Telegram-Bot-Api-Secret-Token
    secret_token = models.CharField(
        max_length=255, default=default_secret_token, editable=False
    )

    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="bots"
    )

    def get_absolute_url(self):
        return reverse("bot_webhook", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.name)


class Chat(ModelBase):
    chat_id = models.CharField(max_length=255)
    chat_info = models.JSONField(default=dict)
    auto_response = models.BooleanField(default=True)

    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="chats")

    def __str__(self):
        return str(self.chat_id)

    @property
    def name(self):
        if self.chat_id.startswith("-"):
            return self.chat_info.get("title", "No Name")
        return (
            self.chat_info.get("first_name")
            or self.chat_info.get("last_name")
            or self.chat_info.get("username", "No Name")
        )

    class Meta:
        ordering = ("-updated_at",)

    def message_list(self, context: str, limit: int = 5):
        l = [
            {"content": m.text, "role": m.get_role_display()}
            for m in self.messages.order_by("-created_at")[:limit]
        ]
        if not any([m.get("role") == RoleChoices.SYSTEM.label for m in l]):
            l = l + [{"content": context, "role": RoleChoices.SYSTEM.label}]
        return l[::-1]


class Message(ModelBase):
    text = models.TextField()
    from_user = models.JSONField(default=dict)
    message_info = models.JSONField(default=dict)
    role = models.IntegerField(choices=RoleChoices.choices, default=RoleChoices.USER)

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")

    def __str__(self):
        return truncatechars(self.text, 32)

    @property
    def sender(self):
        return (
            self.from_user.get("first_name")
            or self.from_user.get("last_name")
            or self.from_user.get("username", "No Name")
        )

    def save(self, *args, **kwargs):
        self.chat.updated_at = self.updated_at
        self.chat.save()
        super().save(*args, **kwargs)


class BotCommand(ModelBase):
    command = models.CharField(
        max_length=32,
        help_text="Command should start with /, contain up to 32 of Latin letters, numbers and underscores",
        validators=[validate_command],
    )
    response = models.TextField()

    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="commands")

    def __str__(self):
        return str(self.command)

    class Meta:
        unique_together = ("bot", "command")


class Predictor(ModelBase):
    api_key = models.CharField("OpenAI API Key", max_length=255)
    context = models.TextField("System Prompt")
    bot = models.OneToOneField(Bot, on_delete=models.CASCADE, related_name="predictor")

    @property
    def api_key_display(self):
        if not self.api_key:
            return "No API Key"
        return self.api_key[:10] + ("." * 38)
