from sqlalchemy.orm import Session
from db.session import get_db
from app.reg.services.outage_service import OutageService
from app.reg.services.location_service import LocationService
from app.reg.services.post_service import PostService


class DatabaseManager:
    """Unified database manager for all services."""

    def __init__(self, db: Session = None):
        self.db = db or next(get_db())
        self.outage_service = OutageService(self.db)
        self.location_service = LocationService(self.db)
        self.post_service = PostService(self.db)

    def close(self):
        """Close database connection"""
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Example usage
if __name__ == "__main__":

    # Test the services
    with DatabaseManager() as db_manager:
        # Test location service
        locations = db_manager.location_service.search_locations("Kigali")
        print(f"Found {len(locations)} locations matching 'Kigali'")

        # Test outage service
        stats = db_manager.outage_service.get_outage_stats()
        print(f"Outage stats: {stats}")

        # Test tweet service
        unprocessed = db_manager.tweet_service.get_unprocessed_tweets(limit=5)
        print(f"Found {len(unprocessed)} unprocessed tweets")
