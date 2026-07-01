import json
from rapidfuzz import process

from app.catalog import load_catalog
from app.retrieval import Retriever
from app.guardrails import (
    is_prompt_injection,
    off_topic,
)
from app.llm import chat
from app.prompts import SYSTEM_PROMPT

retriever = Retriever()
catalog = load_catalog()


def latest_user_message(history):
    for m in reversed(history):
        if m.role == "user":
            return m.content
    return ""


def get_conversation_context(history):
    texts = []

    for m in history:
        if m.role == "user":
            texts.append(m.content)

    return " ".join(texts)


def enrich_query(user):
    q = user.lower()

    if "java" in q:
        return user + " java developer software engineer programming"

    if "python" in q:
        return user + " python developer software engineer programming"

    if "developer" in q:
        return user + " software engineer programming"

    if "software engineer" in q:
        return user + " programming coding technical"

    return user


def compare_assessments(text):
    text_lower = text.lower()

    comparison_words = [
        "compare",
        "difference",
        "differences",
        "versus",
        "vs",
        "between",
    ]

    if not any(
        word in text_lower
        for word in comparison_words
    ):
        return None

    names = [x["name"] for x in catalog]

    matches = process.extract(
        text,
        names,
        limit=5,
    )

    items = []

    for _, score, idx in matches:
        if score > 80:
            items.append(catalog[idx])

    # remove duplicates
    unique = []
    seen = set()

    for item in items:
        if item["name"] not in seen:
            seen.add(item["name"])
            unique.append(item)

    if len(unique) < 2:
        return None

    context = json.dumps(unique[:2])

    prompt = f"""
Compare these assessments:

{context}

Explain:
1. Similarities
2. Differences
3. When each assessment should be used.

Use only the information provided.
"""

    return chat(
        SYSTEM_PROMPT,
        prompt
    )


def build_recommendations(results):
    recommendations = []
    seen = set()

    for x in results:
        name = x["name"]

        if name in seen:
            continue

        seen.add(name)

        recommendations.append(
            {
                "name": name,
                "url": x["link"],
                "test_type": ",".join(
                    x.get("keys", [])
                ),
            }
        )

        if len(recommendations) >= 10:
            break

    return recommendations


def get_personality_assessments(
    query="personality assessment"
):
    docs = retriever.search(
        query,
        top_k=20
    )

    personality_docs = []

    for item in docs:
        keys = ",".join(
            item.get("keys", [])
        ).lower()

        if (
            "personality" in keys
            or "behavior" in keys
            or "competencies" in keys
        ):
            personality_docs.append(item)

    if personality_docs:
        return personality_docs

    # fallback
    docs = []

    for item in catalog:
        keys = ",".join(
            item.get("keys", [])
        ).lower()

        if (
            "personality" in keys
            or "behavior" in keys
        ):
            docs.append(item)

    return docs


def run_agent(history):
    user = latest_user_message(history)
    conversation = get_conversation_context(history)

    # Guardrails
    if is_prompt_injection(user):
        return {
            "reply":
                "I can only discuss SHL assessments.",
            "recommendations": [],
            "end_of_conversation": False,
        }

    if off_topic(user):
        return {
            "reply":
                "I can only answer questions related to SHL assessments and recommendations.",
            "recommendations": [],
            "end_of_conversation": False,
        }

    # Assessment comparison
    compare = compare_assessments(conversation)

    if compare:
        return {
            "reply": compare,
            "recommendations": [],
            "end_of_conversation": False,
        }

    lower = user.lower()

    # Personality recommendations
    if (
        "personality" in lower
        and (
            "add" in lower
            or "include" in lower
            or "update" in lower
            or "recommend" in lower
            or "suggest" in lower
        )
    ):
        return {
            "reply":
                "I updated the recommendations to include personality assessments.",
            "recommendations":
                build_recommendations(
                    get_personality_assessments(user)
                ),
            "end_of_conversation": False,
        }

    # Recommendation search
    query = enrich_query(conversation)

    docs = retriever.search(query)

    # Boost Java assessments
    if "java" in query.lower():
        java_docs = []
        other_docs = []

        for d in docs:
            text = (
                d.get("name", "")
                + " "
                + d.get("description", "")
            ).lower()

            if "java" in text:
                java_docs.append(d)
            else:
                other_docs.append(d)

        docs = java_docs + other_docs

    # Boost Python assessments
    if "python" in query.lower():
        py_docs = []
        other_docs = []

        for d in docs:
            text = (
                d.get("name", "")
                + " "
                + d.get("description", "")
            ).lower()

            if "python" in text:
                py_docs.append(d)
            else:
                other_docs.append(d)

        docs = py_docs + other_docs

    recommendations = build_recommendations(docs)

    if not recommendations:
        return {
            "reply":
                "Could you share the role, skills, experience level, or job description so I can recommend appropriate SHL assessments?",
            "recommendations": [],
            "end_of_conversation": False,
        }

    return {
        "reply":
            "Based on your requirements, I recommend the following assessments.",
        "recommendations":
            recommendations,
        "end_of_conversation": False,
    }