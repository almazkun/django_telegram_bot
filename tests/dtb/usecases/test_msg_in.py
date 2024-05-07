from django.test import TestCase

from dtb.models import Chat, CustomUser, Message
from dtb.usecases.msg_in import MsgIn


class MsgInTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser")
        self.bot = self.user.bots.create(name="TestBot", auth_token="test_token")
        self.telegram_message = {
            "message_id": 1,
            "from": {
                "id": 671559018,
                "is_bot": False,
                "first_name": "Almaz",
                "last_name": "Kunpeissov",
                "username": "akundev",
                "language_code": "en",
            },
            "chat": {
                "id": 671559018,
                "first_name": "Almaz",
                "last_name": "Kunpeissov",
                "username": "akundev",
                "type": "private",
            },
            "date": 1705554449,
            "text": "/start",
            "entities": [{"offset": 0, "length": 6, "type": "bot_command"}],
        }
        self.ws_message = {
            "sender": self.user.username,
            "chat_id": "671559018",
            "text": "Hello, WebSocket!",
        }

    def test_accept_telegram_message(self):
        with self.assertNumQueries(6):
            msg_in = MsgIn()
            msg_in.accept_telegram_message(self.bot, self.telegram_message)
            msg_in.save_message()

        with self.assertNumQueries(3):
            msg_in = MsgIn()
            msg_in.accept_telegram_message(self.bot, self.telegram_message)
            msg_in.save_message()

        chat = Chat.objects.get(chat_id=671559018, bot=self.bot)

        for message in chat.messages.all():
            self.assertEqual(message.text, self.telegram_message["text"])
            self.assertEqual(message.from_user, self.telegram_message["from"])

    def test_accept_websocket_message(self):
        chat = Chat.objects.create(chat_id=671559018, bot=self.bot)
        with self.assertNumQueries(2):
            msg_in = MsgIn()
            msg_in.accept_websocket_message(self.user, chat, self.ws_message["text"])
            msg_in.save_message()

        message = chat.messages.first()
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.text, self.ws_message["text"])
        self.assertEqual(message.from_user["id"], str(self.user.pk))
        self.assertEqual(message.from_user["is_bot"], False)
        self.assertEqual(message.sender, self.user.username)
        self.assertEqual(message.chat, chat)
