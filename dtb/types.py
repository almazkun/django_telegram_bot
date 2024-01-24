"""This module defines types for Telegram and Websocket messages"""
from typing import Any, Dict, List, Optional


class Chat:
    """This class defines the structure of a Telegram chat"""

    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class FromUser:
    """This class defines the structure of a Telegram user"""

    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None


class TelegramMessage:
    """This class defines the structure of a Telegram message"""

    message_id: int
    from_user: FromUser
    chat: Chat
    date: int
    text: Optional[str] = None
    entities: Optional[List[Dict[str, Any]]] = None


class WsTypes:
    """This class defines the types of Websocket messages"""

    CHAT_MESSAGE = "chat_message"
    SYSTEM_NOTIFICATION = "system_notification"
    BOT_MESSAGE = "bot_message"


class WebsocketMessage:
    """This class defines the structure of a Websocket message"""

    sender: str
    text: str
    type: WsTypes
