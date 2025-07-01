from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Any


# Pydantic Models
class OutageType(str, Enum):
    OUTAGE = "outage"
    RESTORATION = "restoration"
    MAINTENANCE = "maintenance"


class OutageStatus(str, Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"
    SCHEDULED = "scheduled"


class Outage(BaseModel):
    id: Optional[int] = None
    tweet_id: str
    areas: List[str]
    outage_type: OutageType
    status: OutageStatus
    timestamp: datetime
    estimated_duration: Optional[str] = None
    cause: Optional[str] = None
    tweet_text: str
    confidence: float = Field(ge=0.0, le=1.0)


class OutageStats(BaseModel):
    total_outages: int
    total_restorations: int
    active_outages: int
    most_affected_areas: List[Dict[str, Any]]
    average_duration: Optional[float] = None


class TwitterConfig(BaseModel):
    bearer_token: str
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str
