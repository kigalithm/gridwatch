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


@water_issue_route.get("/all", response_model=list[WaterIssueOut])
def read_all_water_issues(db: Session = Depends(get_db)):
    issues = crud_water.get_all_issues(db)
    if not issues:
        raise HTTPException(status_code=404, detail="No issues found.")
    return issues
