from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.wasac.models.water_issue import WaterIssue
from app.wasac.schema.water_issue_schema import WaterIssueCreate, WaterIssueUpdate


def create_water_issue(issue: WaterIssueCreate, db: Session):
    water_issue = WaterIssue(**issue.model_dump())
    db.add(water_issue)
    db.commit()
    db.refresh(water_issue)
    return water_issue


def get_all_issues(db: Session):
    return db.query(WaterIssue).order_by(WaterIssue.created_at.desc()).all()
