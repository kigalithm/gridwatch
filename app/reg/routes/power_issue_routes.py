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

water_issue_route = APIRouter(tags=["PowerIssue"])
