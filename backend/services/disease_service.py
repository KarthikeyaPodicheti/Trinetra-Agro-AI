"""Disease Detection service."""

from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ai_engine.disease_detection.inference import get_detector
from backend.models import DiseaseReport, User


async def detect_disease(db: AsyncSession, image_bytes: bytes, crop_type: str,
                         user: Optional[User]) -> Dict[str, Any]:
    detector = get_detector()
    result = detector.predict(image_bytes, crop_type)

    if user and result.get("success"):
        farmer = user.farmer
        report = DiseaseReport(
            farmer_id=farmer.id if farmer else None,
            crop_type=crop_type,
            disease_name=result["disease"],
            confidence=result["confidence"],
            severity=result.get("severity"),
            treatment=result.get("recommendation"),
            prevention_tips=result.get("prevention_tips"),
        )
        db.add(report)
        await db.commit()

    return result
