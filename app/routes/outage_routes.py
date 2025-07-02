from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.models.outage import Outage
from app.db.session import get_db
from app.core.settings import Settings
from fastapi import Request
from datetime import datetime
from app.schema.outage_schema import (
    OutageCreate,
    OutageOut,
)
from app.crud import outage_crud as crud_outage


settings = Settings()

outage_route = APIRouter(tags=["Outage"])


@outage_route.post("/create", response_model=OutageOut, status_code=201)
def create_outage(outage: OutageCreate, db: Session = Depends(get_db)):
    """Create or update outage"""
    return crud_outage.create_outage(outage, db)
