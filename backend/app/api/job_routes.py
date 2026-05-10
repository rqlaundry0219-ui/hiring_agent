from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.job import Job

router = APIRouter()

@router.get("/")
async def get_all_jobs(db: Session = Depends(get_session)):
    return db.exec(select(Job)).all()

@router.post("/")
async def create_job(job: Job, db: Session = Depends(get_session)):
    db.add(job)
    db.commit()
    db.refresh(job)
    return job