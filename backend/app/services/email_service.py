import os
import time

from dotenv import load_dotenv
from groq import Groq
from collections.abc import Generator

from app.models.email import EmailRewriteRequest
from app.prompts.email_rewriter import SYSTEM_PROMPT, build_user_prompt


load_dotenv()


class EmailRewriteService:
    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is not configured.")

        self.client = Groq(api_key=api_key)

    def rewrite_email(self, request: EmailRewriteRequest) -> str:
        user_prompt = build_user_prompt(
            email=request.email,
            tone=request.tone,
        )

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.4,
        )

        rewritten_email = response.choices[0].message.content

        if not rewritten_email:
            raise ValueError("The AI returned an empty response.")

        return rewritten_email.strip()
    
    def stream_rewrite_email(self, request: EmailRewriteRequest)-> Generator[str, None, None]:
        user_prompt = build_user_prompt(
        email=request.email,
        tone=request.tone,
        )
        stream = self.client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.4,
        stream=True,
    )

        for chunk in stream:
            if not chunk.choices:
                continue
            content = chunk.choices[0].delta.content
            if content:
                yield content
                time.sleep(0.05)
        yield "\n"