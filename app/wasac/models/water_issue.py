import uuid
from sqlalchemy import Column, String, ARRAY, Enum, Boolean
from sqlalchemy.dialects.postgresql import JSON
from app.db.base_model import BaseModel
from pgvector.sqlalchemy import Vector
from enum import Enum as PyEnum
from geoalchemy2 import Geometry


class IssueType(str, PyEnum):
    WATER_CUT = "water_cut"
    BROKEN_PIPE = "broken_pipe"
    NEW_COUNTER = "new_counter"


class WaterIssue(BaseModel):
    __tablename__ = "water_issues"
    description = Column(String, nullable=True)
    audio_description = Column(String, nullable=True)
    phone_number = Column(String(20), nullable=True)
    embedding = Column(Vector(384), nullable=False)
    image_url = Column(String, nullable=True)
    is_resolved = Column(Boolean, default=False)
    location = Column(String, nullable=True)
    issue_type = Column(Enum(IssueType), default=IssueType.WATER_CUT, nullable=False)

    coordinates = Column(ARRAY(Geometry("POINT", srid=4326)), nullable=True)
    affected_areas = Column(ARRAY(Geometry("POLYGON")), nullable=True)
    affeccted_area_names = Column(ARRAY(String), nullable=True)
