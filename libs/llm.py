import json
import numpy as np
import pprint
import os
from enum import Enum
from typing import Optional

import openai
from pydantic import BaseModel

client = openai.OpenAI()

if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("OPENAI_API_KEY environment variable not found")


class LlmModel(str, Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"


def llm(*, message: str, system: str = None, examples: list[str] = None) -> str:
    print("=" * 80, "NEW LLM CALL")
    print("=" * 80, "USER MESSAGE")
    print(message)
    messages = []
    if examples is None:
        examples = []
    if system:
        messages.append(
            {
                "role": "system",
                "content": system,
            }
        )
    roles = ["user", "assistant"]
    for i, e in enumerate(examples):
        messages.append(
            {
                "role": roles[i % 2],
                "content": e,
            }
        )
    messages.append({"role": "user", "content": message})
    print("=" * 80, "MESSAGES")
    pprint.pprint(messages)
    completion = client.chat.completions.create(
        model=LlmModel.GPT_3_5_TURBO,
        messages=messages,
    )
    response = completion.choices[0].message.content
    print("=" * 80, "LLM RESPONSE")
    print(response)
    print("=" * 80, "END CALL")
    return response


def cosine_similarity(a, b):
    if b is None:
        return 0
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def rank_relevance_by_similarity(base, others: list):
    print(f"Ranking relevance of {len(others)} entities - {type(base)=})")
    return sorted(
        others, key=lambda x: cosine_similarity(base, x.embedding), reverse=True
    )


def embed_text(text: str):
    print(f"Embedding text {text[:25]}")
    response = client.embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding
