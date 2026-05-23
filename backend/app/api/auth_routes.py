from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, SQLModel, Field
from typing import Optional
from app.core.database import get_session
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

class UserRegister(SQLModel):
    full_name: str = Field(alias="fullName")
    email: str
    password: str
    role: Optional[str] = "seeker"

@router.post("/register")
async def register(user_data: UserRegister, db: Session = Depends(get_session)):
    if not user_data.password:
        raise HTTPException(status_code=400, detail="Password is required")

    existing_user = db.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password=hashed_password,
        role=user_data.role or "seeker"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@router.post("/token")
async def login(username: str, password: str, db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.email == username)).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login")
async def login_oauth(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"} 

