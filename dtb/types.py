"""This module defines types for Telegram and Websocket messages"""

from typing import Any, Dict, List, Optional


class ChatType:
    """ "chat":
    {
        "id": 671559018,
        "first_name": "Almaz",
        "last_name": "Kunpeissov",
        "username": "akundev",
        "type": "private"
    }"""

    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    type: str


class GroupChatType:
    """ "chat":
    {
        "id": -4121165875,
        "title": "Almaz, Akundev",
        "type": "group",
        "all_members_are_administrators": True,
    }"""

    id: int
    title: Optional[str] = None
    type: str
    all_members_are_administrators: Optional[bool] = None


class FromType:
    """ "from":
    {
        "id": 671559018,
        "is_bot": False,
        "first_name": "Almaz",
        "last_name": "Kunpeissov",
        "username": "akundev",
        "language_code": "en"
    }"""

    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None


class TelegramMessage:
    """{
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
        "entities": [{"offset": 0, "length": 6, "type": "bot_command"}]
    }"""

    message_id: int
    from_: FromType
    chat: ChatType
    date: int
    text: Optional[str] = None
    entities: Optional[List[Dict[str, Any]]] = None


class TelegramChatMessage:
    """{
        "message_id": 416,
        "from": {
            "id": 671559018,
            "is_bot": False,
            "first_name": "Almaz",
            "last_name": "Kunpeissov",
            "username": "akundev",
            "language_code": "en",
        },
        "chat": {
            "id": -4121165875,
            "title": "Almaz, Akundev",
            "type": "group",
            "all_members_are_administrators": True,
        },
        "date": 1706157428,
        "text": "/start",
        "entities": [{"offset": 0, "length": 6, "type": "bot_command"}],
    }"""


class WsTypes:
    """This class defines the types of Websocket messages"""

    CHAT_MESSAGE = "chat_message"
    SYSTEM_NOTIFICATION = "system_notification"
    BOT_MESSAGE = "bot_message"


class WebsocketMessage:
    """
    {
        "sender": "Almaz",
        "text": "Hello, WebSocket!",
        "type": "chat_message"
    }
    """

    sender: str
    text: str
    type: WsTypes
