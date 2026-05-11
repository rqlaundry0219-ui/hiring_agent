from openai import AsyncOpenAI
from app.core.config import settings
from fastapi import HTTPException
import os

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def call_llm_structured(system_prompt: str, user_content: str, response_model):
    try:

        response = await client.beta.chat.completions.parse(
        model="gpt-4o-mini", # Use mini to save money during dev!
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        response_format=response_model,
    )
        return response.choices.message.parsed
    except Exception as e:
        print(f"AI ERROR: {e}")
        raise HTTPException(status_code=502, detail="The AI Agent is currently resting. Check credits!")
async def analyze_resume_tool(resume_text: str):
    """Specialized tool for basic resume extraction."""
    from app.agents.prompts import SYSTEM_PROMPT_SCREENING
    from app.agents.models import ResumeAnalysis
    return await call_llm_structured(
        system_prompt=SYSTEM_PROMPT_SCREENING,
        user_content=resume_text,
        response_model=ResumeAnalysis
    )

async def match_jobs_tool(resume_text: str, job_description: str):
    """Specialized tool for matching a resume to a job."""
    from app.agents.prompts import SYSTEM_PROMPT_MATCHING
    from app.agents.models import JobMatch
    content = f"RESUME: {resume_text}\n\nJOB: {job_description}"
    return await call_llm_structured(
        system_prompt=SYSTEM_PROMPT_MATCHING,
        user_content=content,
        response_model=JobMatch
    )
