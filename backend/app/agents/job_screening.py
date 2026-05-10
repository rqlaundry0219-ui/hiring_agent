from app.agents.prompts import SYSTEM_PROMPT_SCREENING
from app.agents.models import ResumeAnalysis
from app.skills.tools import call_llm_structured # We'll build this in skills

class JobScreeningAgent:
    async def screen_candidate(self, resume_text: str):
        # Calls the AI using the prompt and expects the ResumeAnalysis model
        return await call_llm_structured(
            system_prompt=SYSTEM_PROMPT_SCREENING,
            user_content=resume_text,
            response_model=ResumeAnalysis
        )