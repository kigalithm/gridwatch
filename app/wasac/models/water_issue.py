import uuid
from sqlalchemy import Column, String, Float, Text, Enum, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from app.db.base_model import BaseModel


class WaterIssue(BaseModel):
    __tablename__ = "water_issues"
