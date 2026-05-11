from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.models.application import Application

class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str
    location: str
    salary_range: Optional[str] = None
    is_active: bool = Field(default=True)

    # Links a job to all the people who applied
    applications: List["Application"] = Relationship(back_populates="job")