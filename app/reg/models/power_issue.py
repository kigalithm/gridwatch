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
