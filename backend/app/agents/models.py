from pydantic import BaseModel, Field
from typing import List

class ResumeAnalysis(BaseModel):
    summary: str = Field(description="2-sentence professional overview")
    skills_detected: List[str] = Field(description="Key technical skills found")
    recommendations: List[str] = Field(description="3 ways to improve the resume")

class JobMatch(BaseModel):
    match_score: int = Field(ge=0, le=100, description="Score from 0-100")
    explanation: str = Field(description="Detailed reason for this score")