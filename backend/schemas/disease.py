"""Disease Detection schema."""

from pydantic import BaseModel


class DiseaseRequest(BaseModel):
    crop_type: str = "rice"
