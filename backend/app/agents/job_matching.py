from app.agents.prompts import SYSTEM_PROMPT_MATCHING
from app.agents.models import JobMatch
from app.skills.tools import call_llm_structured

class JobMatchingAgent:
    async def match_job(self, resume_text: str, job_description: str):
        content = f"RESUME: {resume_text}\n\nJOB: {job_description}"
        return await call_llm_structured(
            system_prompt=SYSTEM_PROMPT_MATCHING,
            user_content=content,
            response_model=JobMatch
        )