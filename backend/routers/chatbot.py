"""Chatbot router — text chat only (voice removed)."""

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.dependencies import get_db, get_optional_user
from backend.models import User
from backend.schemas.chatbot import ChatRequest, ChatResponse
from backend.services.chatbot_service import get_chatbot

router = APIRouter(prefix="/chat", tags=["chatbot"])


@router.post("/send", response_model=ChatResponse)
async def chat_send(req: ChatRequest, db: AsyncSession = Depends(get_db),
                    user: Optional[User] = Depends(get_optional_user)):
    chatbot = get_chatbot()
    context = None
    if user and user.farmer:
        context = {
            "soil_type": user.farmer.soil_type,
            "land_acres": user.farmer.land_size_acres,
            "location": user.farmer.location,
        }
    reply = await chatbot.chat(req.message, req.session_id, context, req.language)
    return ChatResponse(reply=reply, session_id=req.session_id)


@router.post("/clear")
async def chat_clear(session_id: str = "default"):
    get_chatbot().clear_history(session_id)
    return {"status": "cleared", "session_id": session_id}
