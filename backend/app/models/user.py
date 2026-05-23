from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: str = Field(unique=True, index=True)
    password: str
    role: str = Field(default="seeker")
    is_admin: bool = Field(default=False)
    
    # Links a user to their many applications
    applications: List["Application"] = Relationship(back_populates="user")