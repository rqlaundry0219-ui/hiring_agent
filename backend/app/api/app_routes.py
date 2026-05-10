from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.models.application import Application
from app.agents.job_screening import JobScreeningAgent # Your 'Brain'

router = APIRouter()
agent = JobScreeningAgent()

@router.post("/submit")
async def submit_application(
    job_id: int, 
    user_id: int, 
    resume_text: str, # For now, taking text directly
    db: Session = Depends(get_session)
):
    # 1. Create the application entry
    new_app = Application(job_id=job_id, user_id=user_id, resume_text=resume_text)
    
    # 2. RUN THE AGENT (The 'Real Usage' part)
    # This calls the logic we built in your agents folder
    analysis = await agent.screen_candidate(resume_text)
    
    # 3. Save the Agent's thoughts to the DB
    new_app.match_score = analysis["match_score"]
    new_app.agent_feedback = analysis["decision_logic"]
    
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    
    return {"status": "Application processed", "results": analysis}
