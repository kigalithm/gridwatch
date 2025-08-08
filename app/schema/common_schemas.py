from typing import Optional
from pydantic import BaseModel, Field


class LocationSchema(BaseModel):
    address_text: str = None  # "KN 4 Ave, Kigali City Tower"
    neighborhood: Optional[str] = Field(
        default=None,
        description="Local neighborhood, e.g., 'Kacyiru'",
    )
    landmarks_text: Optional[str] = Field(
        default=None,
        description="Nearby well-known places, e.g., 'near Serena Hotel'",
    )
    maps_url: Optional[str] = None  # Google Maps or OpenStreetMap link
    lat: Optional[float] = None
    lng: Optional[float] = None
    has_exact_location: Optional[bool] = False
    spoken_directions: Optional[str] = Field(
        default=None,
        description="Spoken-style or audio-friendly directions, e.g., 'Opposite Simba Supermarket, behind BK branch'",
    )
