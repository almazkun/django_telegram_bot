import openai


class ChatGPT:
    api_key = 'sk-proj-DBbxPAiAIbSZGW0f0swzT3BlbkFJB9xpoRfIP29l6ASXnb30'
    openai.api_key = api_key

    def __init__(self):
        self.conversation_history = []
        self.max_tokens = 150

    def add_to_context(self, isUser, message):
        self.conversation_history.append("User: " if isUser else "AI: " + message)

    def generateMessage(self):
        # Build prompt with conversation history
        prompt = "\n".join(self.conversation_history)

        # Parameters for the completion
        parameters = {
            "engine": "text-davinci-003",  # Specify the engine, e.g., text-davinci-003
            "max_tokens": self.max_tokens  # Maximum number of tokens to generate
        }

        # Call the completion endpoint
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=None,
            top_p=None,
            frequency_penalty=None,
            presence_penalty=None,
            logprobs=None,
            logit_bias=None,
            echo=False,
            stream=False,
            **parameters
        )

        # Get the generated text from the response
        return response.choices[0].text.strip()

    def send_message(self, message):
        # Add user message to conversation history
        self.add_to_context(True, message)

        # chat gpt answer
        generated_text =  self.generateMessage()

        # Add AI response to conversation history
        self.add_to_context(False, generated_text)

        # Print AI response
        print("AI: " + generated_text)
        return generated_text