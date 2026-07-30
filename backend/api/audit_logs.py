from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.postgres import get_db
from backend.models.schema import SessionLog, AccessAudit
from backend.core.security import verify_password
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

@router.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    # Note: In a real enterprise app, we would inject the current_user from the JWT token
    # and log the AccessAudit here.
    logs = db.query(SessionLog).order_by(SessionLog.timestamp.desc()).all()
    return logs

@router.get("/logs/{session_id}")
def get_log_by_session(session_id: str, db: Session = Depends(get_db)):
    log = db.query(SessionLog).filter(SessionLog.session_id == session_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log
