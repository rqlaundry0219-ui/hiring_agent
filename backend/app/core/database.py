from sqlmodel import create_engine, Session, SQLModel
import os
from dotenv import load_dotenv

# Load variables from the .env file at the root
load_dotenv()

# Use the .db file in your data folder
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/hiring.db")

# The engine is the "bridge" to your SQLite file
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """
    Tells SQLModel to look at your models and build the 
    actual tables inside hiring.db.
    """
    # Import your models here so SQLModel 'sees' them
    from app.models.user import User
    from app.models.job import Job
    from app.models.application import Application
    
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Provides a database session to your API routes.
    """
    with Session(engine) as session:
        yield session
