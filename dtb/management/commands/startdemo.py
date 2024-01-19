from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from dtb.usecases.bot_create import BotCreate

BOT_TOKEN = settings.DEMO_BOT_TOKEN
DOMAIN = settings.DEMO_DOMAIN


class Command(BaseCommand):
    help = "Starts the demo"

    def handle(self, *args, **options):
        self._create_admin()
        self._create_demo_bot()

    def _create_admin(self):
        self.stdout.write(self.style.SUCCESS("Creating admin"))
        try:
            self.admin = get_user_model().objects.create_superuser(
                username="admin", email="admin@example.com", password="admin"
            )
        except Exception:
            self.admin = get_user_model().objects.get(username="admin")

    def _create_demo_bot(self):
        self.stdout.write(self.style.SUCCESS("Creating demo bot"))
        BotCreate(DOMAIN, "Demo Bot", BOT_TOKEN, self.admin).perform()
        self.stdout.write(
            self.style.SUCCESS(
                f"Demo bot is created. Check out {DOMAIN} to see it in action."
            )
        )
