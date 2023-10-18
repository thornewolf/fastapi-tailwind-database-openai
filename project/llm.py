import json
import os
from enum import Enum
from typing import Optional

import openai
from pydantic import BaseModel

openai.api_key = os.getenv("OPENAI_API_KEY")


class LlmModel(str, Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"


class FunctionCallStructure(BaseModel):
    name: str
    arguments: str


class LlmResponse(BaseModel):
    role: str
    content: Optional[str] = None
    function_call: Optional[FunctionCallStructure] = None


def gpt_response(messages: list[dict]) -> tuple[dict, dict]:
    full_response: dict = openai.ChatCompletion.create(
        model=LlmModel.GPT_3_5_TURBO,
        messages=messages,
    )
    message: dict = json.loads(json.dumps(full_response["choices"][0]["message"]))  # type: ignore
    return message


def llm_response(messages: list[dict]) -> LlmResponse:
    return LlmResponse(**gpt_response(messages))


def llm(message: str, system: str = None):
    if system is None:
        return llm_response(
            [
                {
                    "role": "user",
                    "content": message,
                }
            ]
        ).content

    return llm_response(
        [
            {
                "role": "system",
                "content": system,
            },
            {
                "role": "user",
                "content": message,
            },
        ]
    ).content
