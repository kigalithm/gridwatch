from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.db.models.location import Location
from typing import List, Optional, Dict, Tuple
from fuzzywuzzy import fuzz


class LocationService:
    def __init__(self, db: Session):
        self.db = db

    def create_location(self, location_data: Dict) -> Location:
        """Create a new location record"""
        location = Location(**location_data)
        self.db.add(location)
        self.db.commit()
        self.db.refresh(location)
        return location

    def get_location_by_name(self, name: str) -> Optional[Location]:
        """Get location by exact name match"""
        return (
            self.db.query(Location)
            .filter(
                or_(Location.name.ilike(name), Location.name_kinyarwanda.ilike(name))
            )
            .first()
        )

    def search_locations(self, query: str, limit: int = 10) -> List[Location]:
        """Search locations by name with fuzzy matching."""
        # First try exact and partial matches
        exact_matches = (
            self.db.query(Location)
            .filter(
                or_(
                    Location.name.ilike(f"%{query}%"),
                    Location.name_kinyarwanda.ilike(f"%{query}%"),
                )
            )
            .limit(limit)
            .all()
        )

        if exact_matches:
            return exact_matches

        # if no exact matches, do fuzzy matching
        all_locations = self.db.query(Location).all()
        fuzzy_matches = []

        for location in all_locations:
            # Check main name
            score = fuzz.ratio(query.lower(), location.name.lower())
            if location.name_kinyarwanda:
                score = max(
                    score, fuzz.ratio(query.lower(), location.name_kinyarwanda.lower())
                )

            # Check aliases
            if location.aliases:
                for alias in location.aliases:
                    score = max(score, fuzz.ratio(query.lower(), alias.lower()))

            if score > 60:  # Threshold for fuzzy matching
                fuzzy_matches.append((location, score))

        # Sort by score and return top results
        fuzzy_matches.sort(key=lambda x: x[1], reverse=True)
        return [match[0] for match in fuzzy_matches[:limit]]

    def get_locations_by_level(self, level: str) -> List[Location]:
        """Get all locations at a specific administrative level."""
        return self.db.query(Location).filter(Location.level == level).all()

    def get_child_locations(self, parent_name: str, level: str) -> List[Location]:
        """Get child locations under a parent location."""
        if level == "district":
            return (
                self.db.query(Location)
                .filter(
                    Location.parent_province == parent_name,
                    Location.level == "district",
                )
                .all()
            )
        elif level == "sector":
            return (
                self.db.query(Location)
                .filter(
                    Location.parent_district == parent_name, Location.level == "sector"
                )
                .all()
            )
        # Add more levels as needed
        return []
