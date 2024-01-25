from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from dtb.usecases.bot_create import BotCreate

SUPERUSER_USERNAME = settings.SUPERUSER_USERNAME
SUPERUSER_EMAIL = settings.SUPERUSER_EMAIL
SUPERUSER_PASSWORD = settings.SUPERUSER_PASSWORD
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
                username=SUPERUSER_USERNAME,
                email=SUPERUSER_EMAIL,
                password=SUPERUSER_PASSWORD,
            )
        except Exception:
            self.admin = get_user_model().objects.get(username=SUPERUSER_USERNAME)

    def _create_demo_bot(self):
        self.stdout.write(self.style.SUCCESS("Creating demo bot"))
        try:
            bot = BotCreate(BOT_TOKEN).perform(user=self.admin, domain=DOMAIN)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Bot created: {bot.name} ({bot.auth_token})\n"
                    f"Webhook set: {DOMAIN}{bot.get_absolute_url()}\n"
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
            return
