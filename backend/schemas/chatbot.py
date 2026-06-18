"""Schemas for chatbot endpoints."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    session_id: str = "default"
    language: str = "English"


class ChatResponse(BaseModel):
    reply: str
    session_id: str
