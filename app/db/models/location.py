import uuid
from sqlalchemy import Column, String, Float, Integer, Index, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
from app.db.models.base_model import BaseModel


class Location(BaseModel):
    __tablename__ = "locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    level = Column(String)

    parent_province = Column(String, index=True)
    parent_district = Column(String, index=True)
    parent_sector = Column(String)
    parent_cell = Column(String)

    # Geographic data
    coordinates = Column(Geometry("POINT"))
    boundary = Column(Geometry("POLYGON"))

    # Administrative codes
    province_code = Column(String)
    district_code = Column(String)
    sector_code = Column(String)
    cell_code = Column(String)
    village_code = Column(String)

    # Metadata
    population = Column(Integer)
    area_km2 = Column(Float)

    # Data source tracking
    source = Column(String)  # osm, geonames, nisr, custom
    source_id = Column(String)  # Original ID from source

    location_metadata = Column(JSONB, nullable=True)

    # Relationships
    outages = relationship("Outage", back_populates="location")

    __table_args__ = (
        Index("ix_location_name", "name"),
        Index("ix_location_coordinates", "coordinates"),
    )

    # Create composite index for hierarchical queries
    __table_args__ = (
        Index(
            "idx_location_hierarchy",
            "parent_province",
            "parent_district",
            "parent_sector",
        ),
        Index("idx_location_name_level", "name", "level"),
    )

    def __repr__(self):
        return f"<Location(name={self.name}, level={self.level})>"
