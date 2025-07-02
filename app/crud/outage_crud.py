from fastapi import HTTPException
from sqlalchemy.orm import Session
import logging
from app.db.models import Outage
from app.schema import OutageCreate
from sqlalchemy.exc import SQLAlchemyError
from app.dependencies import get_sync_embedding


logger = logging.getLogger(__name__)


def create_outage(outage: OutageCreate, db: Session):
    try:
        outage_dict = outage.model_dump()

        outage_dict["embedding"] = get_outage_embedding(outage)

        db_outage = Outage(**outage_dict)
        db.add(db_outage)
        db.commit()
        db.refresh(db_outage)
        return db_outage
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error creating an outage", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_outage_embedding(
    outage: OutageCreate,
) -> list[float]:
    parts = [
        outage.cause,
        outage.twitter_text,
    ]

    combined_text = " ".join(part for part in parts if part).strip()
    return get_sync_embedding(combined_text)
