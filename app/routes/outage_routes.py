from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.models.outage import Outage
from app.db.session import get_db
from app.core.settings import Settings
from datetime import datetime
from app.schema.outage_schema import (
    OutageCreate,
    OutageOut,
    TwitterConfig,
)
from app.crud import outage_crud as crud_outage
from app.twitter.twitter_client import TwitterClient


settings = Settings()

outage_route = APIRouter(tags=["Outage"])


@outage_route.post("/create", response_model=OutageOut, status_code=201)
def create_outage(outage: OutageCreate, db: Session = Depends(get_db)):
    """Create or update outage"""
    return crud_outage.create_outage(outage, db)


@outage_route.post("/config/twitter")
async def configure_twitter(config: TwitterConfig):
    """Configure Twitter API credentials"""
    global twitter_client
    try:
        twitter_client = TwitterClient(config)
        return {"message": "Twitter API configured successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Twitter configuration failed: {e}"
        )


@outage_route.post("/outages/sync")
async def sync_outages(background_tasks: BackgroundTasks):
    """Sync outages from Twitter"""
    if not twitter_client:
        raise HTTPException(status_code=400, detail="Twitter API not configured")

    background_tasks.add_task(sync_outages_background)
    return {"message": "Outage sync started in background"}


def sync_outages_background():
    pass
