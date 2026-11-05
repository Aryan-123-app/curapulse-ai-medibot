"""HTTP API for the CuraPulse Next.js frontend."""

import logging
import os
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.rag import answer_question

load_dotenv()

logger = logging.getLogger(__name__)
app = FastAPI(title="CuraPulse API")

allowed_origins = os.getenv("FRONTEND_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins if origin.strip()],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    history: list[ChatMessage] = Field(default_factory=list, max_length=40)


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat")
def chat(request: ChatRequest) -> dict[str, object]:
    if not os.getenv("GEMINI_API_KEY"):
        raise HTTPException(status_code=503, detail="GEMINI_API_KEY is not configured.")

    history = [
        ("human" if message.role == "user" else "assistant", message.content)
        for message in request.history
    ]
    try:
        return answer_question(request.question, history)
    except FileNotFoundError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except Exception as error:
        logger.exception("Clinical response generation failed.")
        detail = (
            f"Clinical response failed ({type(error).__name__}). "
            "Check the CuraPulse API terminal for details."
        )
        raise HTTPException(status_code=500, detail=detail) from error
