from app.skills.resume_analysis import analyze_resume_text
from app.skills.job_matching import match_candidate_to_jobs
from app.skills.job_screening import screen_candidate_for_job

class JobAgent:

    def analyze_resume(self, text):
        return analyze_resume_text(text)

    def match_jobs(self, candidate_profile, job_list):
        return match_candidate_to_jobs(candidate_profile, job_list)

    def screen_candidate(self, candidate_profile, job):
        return screen_candidate_for_job(candidate_profile, job)
