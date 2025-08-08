from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from enum import Enum
from datetime import datetime
from app.wasac.models.water_issue import IssueType
from app.schema.common_schemas import LocationSchema


class IssueCreate(BaseModel):
    issue_type: Optional[IssueType] = Field(default=IssueType.WATER_CUT)
    description: Optional[str] = None
    phone_number: Optional[str] = None
    image_url: Optional[str] = None
    location: Optional[LocationSchema] = None
