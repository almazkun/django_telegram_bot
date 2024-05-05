from openai import OpenAI
import os

class ChatGPT:
    api_key = 'sk-proj-DBbxPAiAIbSZGW0f0swzT3BlbkFJB9xpoRfIP29l6ASXnb30'

    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ChatGPT.api_key))
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant."},
        ]

    def add_to_context(self, containt):
        self.messages.append({"role": "system", "content": containt})

    def generateMessage(self, user_message):
        self.messages.append({"role": "user", "content": user_message})

        # Call the completion endpoint
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0,
            max_tokens=1000
        )

        # Get the generated text from the response
        return response.choices[0].message.content