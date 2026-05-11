from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import create_db_and_tables
from app.core.config import settings

from app.api.auth_routes import router as auth_router
from app.api.job_routes import router as job_router
from app.api.app_routes import router as application_router

app = FastAPI(
    title="Hiring Agent API",
    description="Professional AI Agent for Candidate Screening and Job Matching",
    version="1.0.0"
)

# 1. DATABASE STARTUP
# This builds your tables in hiring.db automatically when you start the server
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# 2. CORS MIDDLEWARE
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

# Essential for your React/Vue frontend to connect without "red" errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # In production, replace with your specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(job_router, prefix="/jobs", tags=["Jobs"])
app.include_router(application_router, prefix="/applications", tags=["Applications"])

# 4. HEALTH CHECK
@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "AI Hiring Agent API is Online",
        "database": "Connected",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)