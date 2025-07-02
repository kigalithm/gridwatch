import uuid
from sqlalchemy import Column, String, JSON, ARRAY, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship
from app.db.session import Base
from sqlalchemy import DateTime
from datetime import datetime, timezone
from app.schema.outage_schema import OutageType, OutageStatus


class Outage:
    __tablename__ = "outages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tweet_id = Column(String, nullable=False)
    areas = Column(ARRAY(String), nullable=False)
    outage_type = Column(SqlEnum(OutageType), nullable=False)
    status = Column(SqlEnum(OutageStatus), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    estimated_duration = Column(String, nullable=True)
    cause = Column(String, nullable=True)
    tweet_text = Column(String, nullable=False)
    confidence = Column(String, nullable=False)
    embedding = Column(Vector(384), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=True,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=True,
    )
