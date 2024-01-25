from random import choice

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from dtb.models import Bot

SUPERUSER_USERNAME = settings.SUPERUSER_USERNAME
SUPERUSER_EMAIL = settings.SUPERUSER_EMAIL
SUPERUSER_PASSWORD = settings.SUPERUSER_PASSWORD
BOT_TOKEN = settings.DEMO_BOT_TOKEN
DOMAIN = settings.DEMO_DOMAIN


def generate_message_text():
    return choice(
        [
            "Hello!",
            "Hi!",
            "Hey!",
            "How are you?",
            "Good, and you?",
            "I'm fine, thanks!",
            "What's up?",
            "Dunno, never been there.",
            "What's your name?",
            "My name is Bot.",
            "What's your name?",
            "User",
            "Why would you use async in Django?",
            "Async is useful when you need to make a lot of requests to external services.",
            "What is N+1 problem?",
            "N+1 problem is a performance issue when you make N+1 requests to the database instead of 1.",
            "How to solve N+1 problem in Django?",
            "Use select_related and prefetch_related.",
            "What is the difference between select_related and prefetch_related?",
            "select_related does a SQL join and prefetch_related does 2 SQL queries.",
            "Why django is called batteries included framework?",
            "Because it has a lot of useful features built-in.",
            "What is the difference between Django and Flask?",
            "Django is batteries included framework and Flask is microframework.",
            "What is the difference between Django and DRF?",
            "Django is batteries included framework and DRF is a library for building APIs.",
            "What is SQL injection?",
            "SQL injection is a code injection technique that might destroy your database.",
            "What is the difference between ORM and ODM?",
            "ORM is for relational databases and ODM is for document databases.",
            "What is the difference between SQL and NoSQL?",
            "SQL is relational database and NoSQL is document database.",
            "How to use NoSQL in Django?",
            "Use MongoDB with Djongo.",
            "Why use NoSQL with Django?",
            "Because it is faster. You can use it for analytics. You can use it for machine learning.",
            "What is hardest part of Django?",
            "The hardest part of Django is authentication.",
            "What is the difference between authentication and authorization?",
            "Authentication is about who you are. Authorization is about what you can do.",
            "What is the hardest problem in computer science?",
            "There 2 hard problems in computer science: 2. Naming things. 1. Order guarantee. 3. Off-by-one errors.",
        ]
    )


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
        for i in range(1, 26):
            bot = Bot.objects.create(
                name=f"Bot {i}",
                auth_token=f"token{i}{i}----{i}{i}",
                created_by=self.admin,
            )
            bots.append(bot)
            self.stdout.write(self.style.SUCCESS(f"Bots created: {i}"), ending="\r")
        self.stdout.write(self.style.SUCCESS(f"Bots created: {len(bots)}"))

        for bot in bots:
            for k in range(1, 26):
                chat = bot.chats.create(
                    chat_id=f"chat_id{i}",
                    chat_info={
                        "first_name": self.admin.username
                        if i % 2
                        else f"User {i} very long name he is a very good user",
                    },
                )
                chats.append(chat)
                i += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Chats created: {i}"), ending="\r"
                )
        self.stdout.write(self.style.SUCCESS(f"Chats created: {len(chats)}"))

        for chat in chats:
            for j in range(1, 26):
                message = chat.messages.create(
                    text=generate_message_text(),
                    from_user={
                        "first_name": f"User {i}" if i % 2 else self.admin.username
                    },
                )
                messages.append(message)
                i += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Messages created: {i}"), ending="\r"
                )
        self.stdout.write(self.style.SUCCESS(f"Messages created: {len(messages)}"))
