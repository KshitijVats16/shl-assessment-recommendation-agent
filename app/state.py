def extract_preferences(text):
    prefs = {
        "personality": False,
        "remote": None,
        "max_duration": None,
        "job_level": None,
        "skills": []
    }

    text = text.lower()

    if "personality" in text:
        prefs["personality"] = True

    if "remote" in text:
        prefs["remote"] = True

    if "graduate" in text:
        prefs["job_level"] = "Graduate"

    if "entry" in text:
        prefs["job_level"] = "Entry-Level"

    if "manager" in text:
        prefs["job_level"] = "Manager"

    return prefs