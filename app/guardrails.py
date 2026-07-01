INJECTION_PHRASES = [
    "ignore previous instructions",
    "ignore all instructions",
    "system prompt",
    "reveal prompt",
    "developer message",
    "you are chatgpt",
    "forget previous instructions",
    "act as",
    "jailbreak",
]


def is_prompt_injection(text):
    text = text.lower()

    return any(
        phrase in text
        for phrase in INJECTION_PHRASES
    )


OFF_TOPIC_PHRASES = [
    "fire an employee",
    "terminate employee",
    "legal advice",
    "salary negotiation",
    "dating advice",
    "politics",
    "sports",
]


def off_topic(text):
    text = text.lower()

    return any(
        phrase in text
        for phrase in OFF_TOPIC_PHRASES
    )