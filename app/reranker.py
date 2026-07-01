def rerank_results(results, query):
    q = query.lower()

    scored = []

    for item in results:
        score = 0

        text = (
            item.get("name", "") + " " +
            item.get("description", "") + " " +
            " ".join(item.get("keys", [])) + " " +
            " ".join(item.get("job_levels", []))
        ).lower()

        if "java" in q and "java" in text:
            score += 100

        if "python" in q and "python" in text:
            score += 100

        if "developer" in q and (
            "programming" in text
            or "software" in text
            or "developer" in text
        ):
            score += 30

        if "personality" in q and (
            "personality" in text
            or "behavior" in text
        ):
            score += 100

        if "ability" in q and "ability" in text:
            score += 50

        if "graduate" in q and "graduate" in text:
            score += 40

        if "manager" in q and "manager" in text:
            score += 40

        score += len(
            set(q.split()) &
            set(text.split())
        )

        scored.append((score, item))

    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [x[1] for x in scored]