from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import datetime
from app.wasac.models.water_issue import IssueType
from app.schema.common_schemas import LocationSchema


class WaterIssueCreate(BaseModel):
    issue_type: Optional[IssueType] = Field(default=IssueType.WATER_CUT)
    description: Optional[str] = None
    phone_number: Optional[str] = None
    image_url: Optional[str] = None
    location: Optional[LocationSchema] = None


class WaterIssueUpdate(BaseModel):
    audio_description: str
    location: Optional[LocationSchema] = None
    coordinates: list
    affected_areas: list
    affeccted_area_names: list


class WaterIssueOut(WaterIssueCreate):
    id: UUID
    description: str
    audio_description: str
    is_resolved: bool
    location: LocationSchema
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
