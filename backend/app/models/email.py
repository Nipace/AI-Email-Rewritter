from enum import Enum

from pydantic import BaseModel, Field


class EmailTone(str, Enum):
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    CONCISE = "concise"
    CONFIDENT = "confident"
    POLITE = "polite"

class EmailRewriteRequest(BaseModel):
    email: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="The original email that should be rewritten.",
    )
    tone: EmailTone = Field(
        default=EmailTone.PROFESSIONAL,
        description="The desired tone for the rewritten email.",
    )

class EmailRewriteResponse(BaseModel):
    rewritten_email: str