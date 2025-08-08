from sqlalchemy import Column, String, ARRAY, ForeignKey, Float, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime
from app.reg.schema.outage_schema import OutageType, OutageStatus
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship
from app.db.base_model import BaseModel


class Outage(BaseModel):
    __tablename__ = "outages"
    tweet_id = Column(String, nullable=False)
    tweet_text = Column(String, nullable=False)
    areas = Column(ARRAY(String), nullable=False)
    location_confidence = Column(Float, default=0.0)

    # status tracking
    status = Column(SqlEnum(OutageStatus), nullable=False)
    outage_type = Column(SqlEnum(OutageType), nullable=False)

    # Temporal info
    reported_at = Column(DateTime(timezone=True), nullable=False)
    estimated_start = Column(String, nullable=True)
    estimated_end = Column(DateTime(timezone=True))
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    cause = Column(String, nullable=True)

    # Geographical info
    coordinates = Column(ARRAY(Geometry("POINT", srid=4326)), nullable=True)
    affected_areas = Column(ARRAY(Geometry("POLYGON")), nullable=True)

    embedding = Column(Vector(384), nullable=False)

    source_type = Column(String)
    source_credibility = Column(Float, default=0.5)
    author_id = Column(String)

    # Relationships
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"))
    location = relationship("Location", back_populates="outages")

    def __repr__(self):
        return f"<Outage(id={self.id}, location={self.location_name}, status={self.status})>"
