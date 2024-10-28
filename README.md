# django_telegram_bot
Manage your Telegram Bot with Django

# Functionality
Serve telegram bot (webhook based) with Django
- Allows realtime (websocket) 3 ways communication between Telegram User, Bot and admin with web interface
- Connect ChatGPT to the bot for auto response
- Simple text auto responses for specific keywords
- Multiple bots support
- Admin interface to manage the bot

# Installation
1. Clone the repository
```bash
git clone https://github.com/almazkun/django_telegram_bot
cd django_telegram_bot
```
1. Create a virtual environment and install the dependencies
```bash
pipenv install
pipenv shell
```
1. Create a `.env` file in the root directory and add the following
```bash
cp .env.example .env
```
1. Even for local development, exposed server is required to receive the webhook from Telegram. Use ngrok to expose the server
```bash
ngrok http 8000
```
1. Update the `.env` file with the ngrok url
```bash
DEMO_DOMAIN=https://xxxxxx.ngrok.io
```
1. Run the migrations
```bash
python manage.py migrate
```
1. Create a superuser
```bash
python manage.py createsuperuser
```
1. Run the server
```bash
python manage.py runserver
```


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
