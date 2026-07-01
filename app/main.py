from fastapi import FastAPI

from app.schemas import (
    ChatRequest,
    ChatResponse
)

from app.agent import run_agent

app = FastAPI(
    title="SHL Assessment Agent"
)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):
    response = run_agent(
        request.conversation
    )

    return response