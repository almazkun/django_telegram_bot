# django_telegram_bot
Manage your Telegram Bot with Django

# Deploy
1. Create git tag and push it to the remote repository
Github Actions will build and deploy to the server
```bash
git tag -a v0.1 -m "First release"
git push origin v0.1
```

# Todo
1. Add integration with chat gpt to generate responses
2. Add functionality to bot setting to add 
    1. Chat GPT API key
    2. Set Context (SYSTEM) instructions to the chat responses
3. Add settings to chat to enable/disable the chat gpt responses

# Test Scenario
1. Singup and create a new bot
2. Chat with bot
3. Enable chat gpt responses
4. Chat with bot
5. Disable chat gpt responses
6. Chat with bot
