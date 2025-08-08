from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.wasac.crud import water_issue_crud as crud_water
from app.core.config import Settings
from app.wasac.schema.water_issue_schema import (
    WaterIssueCreate,
    WaterIssueOut,
    WaterIssueUpdate,
)


settings = Settings()

water_issue_route = APIRouter(tags=["WaterIssue"])


@water_issue_route.post("/create", response_model=WaterIssueOut, status_code=201)
def create_water_issue(issue: WaterIssueCreate, db: Session = Depends(get_db)):
    """Create or update outage"""
    return crud_water.create_outage(issue, db)
