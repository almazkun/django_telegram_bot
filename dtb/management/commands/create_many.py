from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from dtb.models import Bot

SUPERUSER_USERNAME = settings.SUPERUSER_USERNAME
SUPERUSER_EMAIL = settings.SUPERUSER_EMAIL
SUPERUSER_PASSWORD = settings.SUPERUSER_PASSWORD
BOT_TOKEN = settings.DEMO_BOT_TOKEN
DOMAIN = settings.DEMO_DOMAIN


class Command(BaseCommand):
    help = "Starts the demo"

    def handle(self, *args, **options):
        self._create_admin()
        self._create_many()

    def _create_admin(self):
        self.stdout.write(self.style.SUCCESS("Creating admin"))
        try:
            self.admin = get_user_model().objects.create_superuser(
                username=SUPERUSER_USERNAME,
                email=SUPERUSER_EMAIL,
                password=SUPERUSER_PASSWORD,
            )
        except Exception:
            self.admin = get_user_model().objects.get(username=SUPERUSER_USERNAME)

    def _create_many(self):
        bots = []
        chats = []
        messages = []
        for i in range(1, 101):
            bot = Bot.objects.create(
                name=f"Bot {i}",
                auth_token=f"token{i}",
                created_by=self.admin,
            )
            bots.append(bot)
            self.stdout.write(self.style.SUCCESS(f"Bots created: {i}"), ending="\r")
        self.stdout.write(self.style.SUCCESS(f"Bots created: {len(bots)}"))

        for bot in bots:
            for i in range(1, 101):
                chat = bot.chats.create(
                    chat_id=f"chat_id{i}",
                    chat_info={"id": f"chat_id{i}"},
                )
                chats.append(chat)
                self.stdout.write(
                    self.style.SUCCESS(f"Chats created: {i}"), ending="\r"
                )
        self.stdout.write(self.style.SUCCESS(f"Chats created: {len(chats)}"))

        for chat in chats:
            for i in range(1, 101):
                message = chat.messages.create(
                    text=f"message {i}",
                    from_user={"id": f"user_id{i}"},
                    message_info={"id": f"message_id{i}"},
                )
                messages.append(message)
                self.stdout.write(
                    self.style.SUCCESS(f"Messages created: {i}"), ending="\r"
                )
        self.stdout.write(self.style.SUCCESS(f"Messages created: {len(messages)}"))
