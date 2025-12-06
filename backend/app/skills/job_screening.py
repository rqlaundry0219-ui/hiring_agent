# hiring_agent\backend/app/skills/job_screening.py

def screen_candidate(text: str):
    required = ["leadership", "management", "sales", "communication"]

    detected = [skill for skill in required if skill in text.lower()]

    score = int((len(detected) / len(required)) * 100)

    decision = "Recommended" if score >= 50 else "Not Recommended"

    return {
        "match_score": score,
        "decision": decision,
        "notes": f"Candidate matched {len(detected)} out of {len(required)} required skills."
    }