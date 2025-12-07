from backend.app.skills.resume_analysis import analyze_resume_text
from backend.app.skills.job_matching import match_candidate_to_jobs
from backend.app.skills.job_screening import screen_candidate


class JobAgent:

    def analyze_resume(self, text):
        return analyze_resume_text(text)

    def match_jobs(self, candidate_profile, job_list):
        return match_candidate_to_jobs(candidate_profile, job_list)

    def screen_candidate(self, candidate_profile, job):
        return screen_candidate(candidate_profile, job)
