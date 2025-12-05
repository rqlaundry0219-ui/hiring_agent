FAKE_JOB_DB = [
    {"title": "Sales Associate", "skills": ["sales", "communication", "customer service"]},
    {"title": "Team Lead", "skills": ["leadership", "communication"]},
    {"title": "Retail Manager", "skills": ["management", "customer service", "leadership"]},
]

def match_candidate_to_jobs(skills: list):
    matching_jobs = []

    for job in FAKE_JOB_DB:
        overlap = set(skills).intersection(job["skills"])
        if overlap:
            matching_jobs.append({
                "job_title": job["title"],
                "matching_skills": list(overlap),
                "match_count": len(overlap)
            })

    return matching_jobs
