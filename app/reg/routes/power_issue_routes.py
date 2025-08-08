from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.reg.crud import power_issue_crud as crud_power
from app.core.config import Settings
from app.reg.schema.power_issue_schema import (
    PowerIssueCreate,
    PowerIssueOut,
    powerIssueUpdate,
)


settings = Settings()

power_issue_route = APIRouter(tags=["PowerIssue"])


@power_issue_route.post("/create", response_model=PowerIssueOut, status_code=201)
def create_power_issue(issue: PowerIssueCreate, db: Session = Depends(get_db)):
    """Create or update an issue"""
    return crud_power.create_power_issue(issue, db)


@power_issue_route.get("/all", response_model=list[PowerIssueOut])
def read_all_power_issues(db: Session = Depends(get_db)):
    issues = crud_power.get_all_issues(db)
    if not issues:
        raise HTTPException(status_code=404, detail="No issues found.")
    return issues
