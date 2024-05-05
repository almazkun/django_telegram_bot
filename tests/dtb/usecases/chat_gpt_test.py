from django.test import TestCase
from dtb.providers.chat_gpt import ChatGPT


class ChatGptTestCase(TestCase):
    def setUp(self):
        self.chat_gpt = ChatGPT()

    def test_simple_context(self):
        answer = self.chat_gpt.generateMessage("Translate to French a word Victory. Show me only the translated word")
        self.assertEqual(answer, "Victoire")

    def test_realistic_context(self):
        chat_gpt = ChatGPT()
        context = """
        Context: Large sports store. There are three main branches: football, boxing, swimming. 
        Each of the departments has areas for men and women, who in turn are divided by age: adult children. 

        Telephone extensions for all venues:

        Football Department:

        Men:
        Adults: +041122377111
        Children: +041122377112
        Women:
        Adults: +041122377121
        Children: +041122377122

        Boxing Department:

        Men:
        Adults: +041122377211
        Children: +041122377212
        Women:
        Adults: +041122377221
        Children: +041122377222

        Swimming Department:

        Men:
        Adults: +041122377311
        Children: +041122377312
        Women:
        Adults: +041122377321
        Children: +041122377322
        """

        chat_gpt.add_to_context(context)
        answer = chat_gpt.generateMessage("I want to get advice on fins for a 12 year old girl. "
                                          "I want to see your answer where will be only phone number without other words!")

        self.assertEqual(answer, "+041122377322")
