from fastapi import FastAPI
from app.agents.job_agent import JobAgent

app = FastAPI()

# Initialize your AI Hiring Agent
agent = JobAgent()

@app.get("/")
def home():
    return {"message": "AI Hiring Agent API is running!"}

@app.post("/analyze-resume")
def analyze_resume(data: dict):
    resume_text = data.get("resume", "")
    return agent.analyze_resume(resume_text)

@app.post("/match-jobs")
def match_jobs(data: dict):
    candidate = data.get("candidate", {})
    jobs = data.get("jobs", [])
    return agent.match_jobs(candidate, jobs)

@app.post("/screen-candidate")
def screen_candidate(data: dict):
    candidate = data.get("candidate", {})
    job = data.get("job", {})
    return agent.screen_candidate(candidate, job)
