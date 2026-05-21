"""Disease Detection router — accepts raw image bytes via JSON base64."""
import base64
from typing import Optional

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.dependencies import get_db, get_optional_user
from backend.models import User
from backend.services.disease_service import detect_disease

router = APIRouter(prefix="/ai", tags=["disease"])


@router.post("/disease")
async def disease_detect(
    crop_type: str = "rice",
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    if image is None:
        return {"error": "No image uploaded"}
    image_bytes = await image.read()
    if len(image_bytes) < 100:
        return {"error": "Image too small or invalid"}
    return await detect_disease(db, image_bytes, crop_type, user)
