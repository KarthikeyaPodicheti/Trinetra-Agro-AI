"""Feedback router."""

from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.dependencies import get_db, get_optional_user
from backend.models import Feedback, User

router = APIRouter(prefix="/feedback", tags=["feedback"])


class FeedbackRequest(BaseModel):
    feature: str = Field(..., min_length=1, max_length=100)
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=1)


@router.post("")
async def submit_feedback(req: FeedbackRequest, db: AsyncSession = Depends(get_db),
                          user: Optional[User] = Depends(get_optional_user)):
    fb = Feedback(
        user_id=user.id if user else None,
        feature=req.feature,
        rating=req.rating,
        comment=req.comment,
    )
    db.add(fb)
    await db.commit()
    return {"success": True, "message": "Feedback submitted"}
