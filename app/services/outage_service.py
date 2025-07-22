from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app.db.models.outage import Outage
from app.db.models.location import Location
from app.db.models.post import Post
from typing import List, Optional, Dict
from datetime import datetime, timedelta, timezone


class OutageService:
    def __init__(self, db: Session):
        self.db = db

    def create_outage(self, outage_data: Dict) -> Outage:
        """Create a new outage record."""
        outage = Outage(**outage_data)
        self.db.add(outage)
        self.db.commit()
        self.db.refresh(outage)
        return outage

    def get_outage_by_tweet_id(self, tweet_id: str) -> Optional[Outage]:
        """Retrieve an outage by its tweet ID."""
        return self.db.query(Outage).filter(Outage.tweet_id == tweet_id).first()

    def get_active_outages(self) -> List[Outage]:
        """Get all active (unresolved) outages."""
        return (
            self.db.query(Outage)
            .filter(Outage.status.in_(["reported", "confirmed"]))
            .all()
        )

    def get_outages_by_location(self, location_name: str) -> List[Outage]:
        """Get outages associated with a specific location."""
        return (
            self.db.query(Outage)
            .filter(Outage.location_name.ilike(f"%{location_name}%"))
            .all()
        )

    def get_recent_outages(self, hours: int = 24) -> List[Outage]:
        """Get outages reported in the last specified hours."""
        cutoff_time = datetime.now(timezone.now()) - timedelta(hours=hours)
        return (
            self.db.query(Outage)
            .filter(Outage.reported_at >= cutoff_time)
            .order_by(Outage.reported_at.desc())
            .all()
        )

    def update_outage_status(self, outage_id: str, status: str) -> Optional[Outage]:
        """Update the status of an outage"""
        outage = self.db.query(Outage).filter(Outage.id == outage_id).first()
        if outage:
            outage.status = status
            if status == "resolved":
                outage.resolved_at = datetime.now(timezone.now())
            self.db.commit()
            self.db.refresh(outage)
        return outage

    def get_outage_stats(self) -> Dict:
        """Get basic outage statistics."""
        total_outages = self.db.query(Outage).count()
        active_outages = (
            self.db.query(Outage)
            .filter(Outage.status.in_(["reported", "confirmed"]))
            .count()
        )
        resolved_outages = (
            self.db.query(Outage).filter(Outage.status == "resolved").count()
        )
        return {
            "total_outages": total_outages,
            "active_outages": active_outages,
            "resolved_outages": resolved_outages,
            "last_updated": datetime.now(timezone.now()).isoformat(),
        }
