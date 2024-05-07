from django.test import TestCase

from dtb.models import Bot, Chat, CustomUser, Predictor, RoleChoices


class TestModels(TestCase):
    def test_chat(self):
        user = CustomUser.objects.create(username="testuser")
        bot = Bot.objects.create(
            name="TestBot",
            created_by=user,
        )
        predictor = Predictor.objects.create(
            api_key="test_key", context="Test context", bot=bot
        )
        chat = Chat.objects.create(chat_id="1", bot=bot)

        for i in range(10):
            chat.messages.create(text=f"Message {i}", role=1 if i % 2 == 0 else 2)

        limit = 5

        messages = chat.message_list(predictor.context, limit)

        self.assertEqual(len(messages), limit + 1)
        self.assertEqual(messages[0]["role"], RoleChoices.SYSTEM.label)
        self.assertEqual(messages[0]["content"], predictor.context)
        self.assertEqual(messages[1]["role"], RoleChoices.USER.label)
        self.assertEqual(messages[1]["content"], "Message 5")
        self.assertEqual(messages[2]["role"], RoleChoices.ASSISTANT.label)
        self.assertEqual(messages[2]["content"], "Message 6")
        self.assertEqual(messages[3]["role"], RoleChoices.USER.label)
        self.assertEqual(messages[3]["content"], "Message 7")
        self.assertEqual(messages[4]["role"], RoleChoices.ASSISTANT.label)
        self.assertEqual(messages[4]["content"], "Message 8")
        self.assertEqual(messages[5]["role"], RoleChoices.USER.label)
        self.assertEqual(messages[5]["content"], "Message 9")
