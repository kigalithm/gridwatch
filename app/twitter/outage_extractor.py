import logging
import re
import spacy
from datetime import datetime
from typing import List, Optional

from app.schema.outage_schema import (
    Outage,
    OutageStatus,
    OutageType,
)


class OutageExtractor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Try to load spacy model, fallback to basic processing if not available
        try:
            self.nlp = spacy.load("en_core_web_sm")
            self.logger.info("☑️ spaCy model loaded.")
        except OSError:
            self.logger.warning("spaCy model not found. Using basic text processing.")
            self.nlp = None

        # Rwanda locations (extend this list as needed)
        self.rwanda_locations = {
            "kigali",
            "butare",
            "gitarama",
            "ruhengeri",
            "gisenyi",
            "cyangugu",
            "kibungo",
            "byumba",
            "gikongoro",
            "kibuye",
            "umutara",
            "gasabo",
            "kicukiro",
            "nyarugenge",
            "muhanga",
            "musanze",
            "rubavu",
            "rusizi",
            "nyagatare",
            "kayonza",
            "rwamagana",
            "bugesera",
            "nyanza",
            "gisagara",
            "nyaruguru",
            "huye",
            "nyamagabe",
            "ruhango",
            "kamonyi",
            "rulindo",
            "gakenke",
            "burera",
            "gicumbi",
            "kirehe",
            "ngoma",
            "gatsibo",
        }

        # Outage keywords
        self.outage_keywords = {
            "outage": [
                "outage",
                "blackout",
                "power cut",
                "electricity off",
                "no power",
                "power failure",
            ],
            "restoration": [
                "restored",
                "power back",
                "electricity restored",
                "back online",
                "service resumed",
            ],
            "maintenance": [
                "maintenance",
                "scheduled",
                "planned",
                "upgrade",
                "repairs",
            ],
        }

        # Cause keywords
        self.cause_keywords = {
            "technical": ["technical", "equipment", "transformer", "cable", "fault"],
            "weather": ["storm", "rain", "wind", "weather", "lightning"],
            "maintenance": ["maintenance", "upgrade", "repair", "inspection"],
            "load": ["overload", "high demand", "capacity"],
        }

    def extract_locations(self, text: str) -> List[str]:
        """Extract Rwanda locations from text"""
        text_lower = text.lower()
        found_locations = []

        for location in self.rwanda_locations:
            if location in text_lower:
                found_locations.append(location.title())

        # Use spaCy for additional location extraction if available
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in ["GPE", "LOC"]:  # Geopolitical entity or Location
                    location_clean = ent.text.lower().strip()
                    if location_clean not in [loc.lower() for loc in found_locations]:
                        found_locations.append(ent.text.title())

        return found_locations

    def classify_outage_type(self, text: str) -> tuple[OutageType, float]:
        """Classify the type of outage and return confidence score"""
        text_lower = text.lower()
        scores = {}

        for outage_type, keywords in self.outage_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                scores[outage_type] = score / len(keywords)

        if not scores:
            return OutageType.OUTAGE, 0.3  # Default with low confidence

        best_type = max(scores, key=scores.get)
        confidence = scores[best_type]

        return OutageType(best_type), min(confidence, 1.0)

    def extract_cause(self, text: str) -> Optional[str]:
        """Extract the likely cause of the outage"""
        text_lower = text.lower()

        for cause_type, keywords in self.cause_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return cause_type

        return None

    def extract_duration(self, text: str) -> Optional[str]:
        """Extract estimated duration from text"""
        # Look for time patterns
        time_patterns = [
            r"(\d+)\s*hours?",
            r"(\d+)\s*minutes?",
            r"(\d+)\s*hrs?",
            r"(\d+)\s*mins?",
        ]

        for pattern in time_patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(0)

        return None

    def process_tweet(self, tweet_text: str, tweet_id: str) -> Optional[Outage]:
        """Process a tweet and extract outage information"""
        locations = self.extract_locations(tweet_text)
        if not locations:
            return None

        outage_type, confidence = self.classify_outage_type(tweet_text)
        cause = self.extract_cause(tweet_text)
        duration = self.extract_duration(tweet_text)

        # Determine status based on type
        if outage_type == OutageType.RESTORATION:
            status = OutageStatus.RESOLVED
        elif outage_type == OutageType.MAINTENANCE:
            status = OutageStatus.SCHEDULED
        else:
            status = OutageStatus.ACTIVE

        # Use the first location found (could be improved to handle multiple)
        area = locations[0]

        return Outage(
            tweet_id=tweet_id,
            area=area,
            outage_type=outage_type,
            status=status,
            timestamp=datetime.now(),
            estimated_duration=duration,
            cause=cause,
            tweet_text=tweet_text,
            confidence=confidence,
        )
