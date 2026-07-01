def apply_filters(docs, prefs):
    results = docs

    if prefs["personality"]:
        results = [
            x for x in results
            if "Personality"
            in ",".join(x.get("keys", []))
        ]

    if prefs["remote"]:
        results = [
            x for x in results
            if x.get("remote") == "yes"
        ]

    if prefs["job_level"]:
        results = [
            x for x in results
            if prefs["job_level"]
            in x.get("job_levels", [])
        ]

    return results