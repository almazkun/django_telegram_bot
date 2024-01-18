from django.core.management.base import BaseCommand

from dtb.models import TelegramBot

from django.conf import settings

BOT_TOKEN = settings.DEMO_BOT_TOKEN
DOMAIN = settings.DEMO_DOMAIN


class Command(BaseCommand):
    help = "Starts the demo"

    def handle(self, *args, **options):
        self._create_demo_bot()

    def _create_demo_bot(self):
        self.stdout.write(self.style.SUCCESS(f"Creating demo bot for {BOT_TOKEN}"))
        self.bot = TelegramBot.objects.create(auth_token=BOT_TOKEN)
        r = self.bot.set_webhook(f"{DOMAIN}{bot.get_absolute_url()}")
        self.stdout.write(self.style.SUCCESS(r))

    def _create_start_command(self):
        self.stdout.write(self.style.SUCCESS("Creating start command"))
        self.bot.commands.create(command="/start", response="Hello, world!")
