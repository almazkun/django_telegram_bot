# django_telegram_bot
Manage your Telegram Bot with Django

# Deploy
1. Create git tag and push it to the remote repository
Github Actions will build and deploy to the server
```bash
git tag -a v0.1 -m "First release"
git push origin v0.1
```

# Usage
1. Create a new Telegram Bot
    - open telegram application in IOS or Android https://telegram.org/apps
    - search for BotFather
    - create a new bot by sending the command /newbot
    - Type `NameOfTheBot` and copy the token
1. Sign Up on https://bot.akun.dev/accounts/signup/
    - Username and Password is required
    - Login with the username and password
    - Create a new bot with the token from BotFather
    - After creating the bot you will see the bot in the list
1. Chat With your bot
    - Open telegram application and search for the `NameOfTheBot` you created
    - Click start. You should see the Welcome message.
    - Reload the https://bot.akun.dev/ and click on your bot name
    - You should see messages from yourself!
    - Make some back and forth messages with the bot
1. Connect ChatGPT auto response
    - Go to https://platform.openai.com/signup and sign up
    - Generate the API key https://platform.openai.com/api-keys
    - Copy the API key
    - Open the bot on https://bot.akun.dev/
    - Click on the bot name
    - Click on the `Bot/Chat Settings` button
    - Paste the API key in the `OpenAI API Key` field and click Connect ChatGPT
1. Chat with the bot
    - Open the telegram application and chat with the bot
    - The bot should respond with the ChatGPT response
