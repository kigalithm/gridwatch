from sqlalchemy import Column, String, ARRAY, Enum, Boolean, Float
from sqlalchemy.dialects.postgresql import JSON
from app.db.base_model import BaseModel
from pgvector.sqlalchemy import Vector
from enum import Enum as PyEnum
from geoalchemy2 import Geometry


class IssueType(str, PyEnum):
    OUTAGE = "outage"
    BROKEN_STREET_LIGHTS = "broken_street_lights"
    POTENTIALLY_FATAL = "potentially_fatal"


class PowerIssue(BaseModel):
    __tablename__ = "power_issues"
    description = Column(String, nullable=True)
    audio_description = Column(String, nullable=True)
    phone_number = Column(String(20), nullable=True)
    embedding = Column(Vector(384), nullable=False)
    image_url = Column(String, nullable=True)
    is_resolved = Column(Boolean, default=False)
    location = Column(JSON, nullable=True)
    issue_type = Column(Enum(IssueType), default=IssueType.OUTAGE, nullable=False)
    approx_lat = Column(Float, nullable=True)
    approx_long = Column(Float, nullable=True)
    affected_areas = Column(ARRAY(Geometry("POLYGON")), nullable=True)
    affeccted_area_names = Column(ARRAY(String), nullable=True)
