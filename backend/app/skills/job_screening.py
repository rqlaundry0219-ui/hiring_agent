def screen_candidate(candidate_profile: dict, job: dict):

    text = (candidate_profile.get("experience", "") + " " +
            candidate_profile.get("skills", ""))

    required = ["leadership", "management", "sales", "communication"]

    detected = [skill for skill in required if skill.lower() in text.lower()]

    score = int((len(detected) / len(required)) * 100)

    decision = "Recommended" if score >= 50 else "Not Recommended"

    return {
        "match_score": score,
        "decision": decision,
        "notes": f"Candidate matched {len(detected)} out of {len(required)} required skills."
    }
