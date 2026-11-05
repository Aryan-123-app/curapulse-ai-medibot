"""Shared retrieval-augmented clinical answer generation."""

import importlib
import os
from functools import lru_cache
from pathlib import Path

from src.prompt import CONTEXTUALIZE_Q_SYSTEM_PROMPT, SYSTEM_PROMPT

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@lru_cache(maxsize=1)
def load_retriever(k: int = 4):
    """Load the local Chroma retriever once for the API process."""
    from src.helper import download_embedding

    configured_dir = Path(os.getenv("CHROMA_PERSIST_DIR", "vectorstore"))
    persist_dir = (
        configured_dir
        if configured_dir.is_absolute()
        else PROJECT_ROOT / configured_dir
    )
    if not persist_dir.is_dir() or not any(persist_dir.iterdir()):
        raise FileNotFoundError(
            "Local Chroma vector store not found. Run `python ingest.py --store chroma` first."
        )

    try:
        from langchain_chroma import Chroma
    except ImportError:
        Chroma = importlib.import_module("langchain_community.vectorstores").Chroma

    vectorstore = Chroma(
        persist_directory=str(persist_dir),
        embedding_function=download_embedding(),
    )
    return vectorstore.as_retriever(search_kwargs={"k": k})


def answer_question(
    question: str,
    chat_history: list[tuple[str, str]],
) -> dict[str, object]:
    """Run the same history-aware Gemini and Chroma RAG flow used by the app."""
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_google_genai import ChatGoogleGenerativeAI

    try:
        from langchain_classic.chains import (
            create_history_aware_retriever,
            create_retrieval_chain,
        )
        from langchain_classic.chains.combine_documents import create_stuff_documents_chain
    except ImportError:
        chains = importlib.import_module("langchain.chains")
        combine_documents = importlib.import_module("langchain.chains.combine_documents")
        create_history_aware_retriever = chains.create_history_aware_retriever
        create_retrieval_chain = chains.create_retrieval_chain
        create_stuff_documents_chain = combine_documents.create_stuff_documents_chain

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.2,
    )
    retriever = load_retriever()

    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", CONTEXTUALIZE_Q_SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    response = rag_chain.invoke({"input": question, "chat_history": chat_history})

    sources = [
        {
            "source": document.metadata.get(
                "source", "The Gale Encyclopedia of Medicine"
            ),
            "page": document.metadata.get("page", "Unknown"),
            "excerpt": document.page_content[:260].replace("\n", " ").strip() + "...",
        }
        for document in response.get("context", [])
    ]
    return {"answer": response.get("answer", ""), "sources": sources}
