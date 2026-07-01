from openai import OpenAI
from app.config import settings


client = OpenAI(
    api_key=settings.API_KEY,
    base_url=settings.BASE_URL
)


def chat(system, user):
    response = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": system,
            },
            {
                "role": "user",
                "content": user,
            }
        ],
        temperature=0
    )

    return (
        response
        .choices[0]
        .message
        .content
    )