from typing import Dict, List

from asgiref.sync import async_to_sync
from openai import AsyncAPIResponse, AsyncOpenAI


async def chat_complete(
    message_list: List[Dict],
    model: str,
    api_key: str,
) -> AsyncAPIResponse:
    """Get a response from OpenAI.
    https://platform.openai.com/docs/guides/gpt/chat-completions-api

    Args:
        messages: A list of messages from the user and the bot.
        model: The name of the model to use.
        api_key: The API key to use.

    Returns:
        ```{
            "id": "chatcmpl-qwerefsd",
            "choices": [
                {
                    "finish_reason": "stop",
                    "index": 0,
                    "logprobs": null,
                    "message": {
                        "content": "Great!.",
                        "role": "assistant",
                    }
                }
            ],
            "created": 1714547383,
            "model": "gpt-3.5-turbo-0125",
            "object": "chat.completion",
            "system_fingerprint": "fp_3b956da36b",
            "usage": {
                "completion_tokens": 93,
                "prompt_tokens": 234,
                "total_tokens": 327
            }
        }
        ```
    """
    client = AsyncOpenAI(api_key=api_key)
    return await client.chat.completions.create(model=model, messages=message_list)


async def generate_response(
    message_list: list,
    model_name: str,
    api_key: str,
) -> str:
    response = async_to_sync(chat_complete)(
        message_list,
        model_name,
        api_key,
    )
    return response.choices[0].message.content
