import json
import logging
import urllib.request
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


def run_in_executor(func):
    def wrapper(*args, **kwargs):
        return ThreadPoolExecutor().submit(func, *args, **kwargs)

    return wrapper


class TelegramBotClient:
    def __init__(self, auth_token):
        self.auth_token = auth_token

    @run_in_executor
    def _url_open(self, method, path, data):
        full_url = f"https://api.telegram.org/bot{self.auth_token}/{path}"
        req = urllib.request.Request(full_url, method=method)
        req.add_header("Content-Type", "application/json; charset=utf-8")
        json_data = json.dumps(data)
        json_data = json_data.encode("utf-8")
        req.add_header("Content-Length", len(json_data))
        logger.debug(
            f"TelegramBotClient._url_open: Sending request to {full_url}, data: {json_data}"
        )
        with urllib.request.urlopen(req, json_data, timeout=10) as f:
            status_code = f.getcode()
            response = f.read().decode("utf-8")
            logger.debug(
                f"TelegramBotClient._url_open: Received response {status_code} {response}"
            )
            if status_code != 200:
                raise Exception(
                    f"TelegramBotClient._url_open: {status_code} {response}"
                )
            return json.loads(response)

    def _post(self, path, data):
        return self._url_open("POST", path, data)

    def set_webhook(self, url, secret_token):
        """https://core.telegram.org/bots/api#setwebhook

        POST https://api.telegram.org/bot{token}/setWebhook?url={url}&secret_token={secret_token}

        :param url: HTTPS url to send updates to. Use an empty string to remove webhook integration
        :param secret_token: Optional. If specified, the request will be sent with a header of
                             X-Telegram-Bot-Api-Secret-Token containing the value of the field
                             secret_token

        :return: `{'ok': True, 'result': True, 'description': 'Webhook was set'}`
        """
        return self._post(
            "setWebhook",
            {
                "url": url,
                "allowed_updates": ["message"],
                "secret_token": secret_token,
            },
        )

    def send_message(self, chat_id, text):
        """https://core.telegram.org/bots/api#sendmessage

        POST https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}

        :param chat_id: Unique identifier for the target chat or username of the target
                        channel (in the format @channelusername)
        :param text: Text of the message to be sent

        :return: ```{
            "update_id": 465319158,
            "message": {
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
            },
        }```
        """
        return self._post(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": text,
            },
        )

    def send_typing(self, chat_id):
        """https://core.telegram.org/bots/api
        POST https://api.telegram.org/bot{token}/sendChatAction?chat_id={chat_id}&action=typing

        :param chat_id: Unique identifier for the target chat or username of
                        the target channel (in the format @channelusername)

        :return: `{'ok': True, 'result': True, 'description': 'Webhook was set'}`
        """
        return self._post(
            "sendChatAction",
            {
                "chat_id": chat_id,
                "action": "typing",
            },
        )

    def get_me(self):
        """https://core.telegram.org/bots/api
        POST https://api.telegram.org/bot{token}/getMe

        :return: ```{
            "ok": True,
            "result": {
                "id": 6793918636,
                "is_bot": True,
                "first_name": "Akundev",
                "username": "akundev_bot",
                "can_join_groups": True,
                "can_read_all_group_messages": True,
                "supports_inline_queries": False,
            },
        }```
        """
        return self._post("getMe", {})
