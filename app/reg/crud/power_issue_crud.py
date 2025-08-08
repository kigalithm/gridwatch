from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.reg.models.power_issue import PowerIssue
from app.reg.schema.power_issue_schema import PowerIssueCreate, PowerIssueUpdate
from app.db.db_manager import get_db


def create_power_issue(issue: PowerIssueCreate, db: Session):
    power_issue = PowerIssue(**issue.model_dump())
    db.add(power_issue)
    db.commit()
    db.refresh(power_issue)
    return power_issue


def get_all_issues(db: Session):
    return db.query(PowerIssue).order_by(PowerIssue.created_at.desc()).all()
