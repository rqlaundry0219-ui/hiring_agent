from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from enum import Enum

class ApplicationStatus(str, Enum):
    applied = "applied"
    screening = "screening"
    interview = "interview"
    rejected = "rejected"

class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    job_id: int = Field(foreign_key="job.id")
    
    status: ApplicationStatus = Field(default=ApplicationStatus.applied)
    
    # AGENT FIELDS: Where the AI stores its work
    match_score: Optional[int] = None
    agent_feedback: Optional[str] = None # Why the AI liked/disliked them
    resume_text: Optional[str] = None    # Extracted text for the AI to read

    # Relationships back to User and Job
    user: Optional["User"] = Relationship(back_populates="applications")
    job: Optional["Job"] = Relationship(back_populates="applications")
