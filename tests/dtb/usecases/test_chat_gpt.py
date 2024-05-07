from django.test import TestCase
from openai import AuthenticationError

from dtb.providers.chat_gpt import generate_response


class ChatGptTestCase(TestCase):
    def test_simple_context(self):
        message_list = [
            {
                "text": "Hello",
                "role": "user",
            },
            {
                "text": "Hi",
                "role": "system",
            },
        ]
        model_name = "gpt-3.5-turbo"
        api_key = "sk-proj-1234567890123456789012345678901234567890"

        self.assertRaises(
            AuthenticationError,
            generate_response,
            message_list,
            model_name,
            api_key,
        )
