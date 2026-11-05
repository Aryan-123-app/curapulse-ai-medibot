"""
Data loading, preprocessing, embedding, and vector-store helper module for CuraPulse AI.
"""

import os
from typing import List, Optional
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


import glob

def load_pdf_documents(data_dir: str = "data", limit: Optional[int] = None) -> List[Document]:
    """
    Loads PDF documents from the specified directory, preserving
    vital metadata like page numbers and source filenames.
    Supports lazy loading with limit for fast testing.
    """
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory '{data_dir}' not found.")

    pdf_files = glob.glob(os.path.join(data_dir, "*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in '{data_dir}'.")

    documents: List[Document] = []
    for pdf_path in pdf_files:
        print(f"Reading '{os.path.basename(pdf_path)}'...")
        loader = PyPDFLoader(pdf_path)
        for doc in loader.lazy_load():
            documents.append(doc)
            if limit and len(documents) >= limit:
                print(f"Reached page limit ({limit}).")
                return documents

    print(f"Loaded {len(documents)} document pages from '{data_dir}'.")
    return documents



def filter_and_clean_docs(docs: List[Document]) -> List[Document]:
    """
    Cleans document contents and retains critical citation metadata:
    source filename and page number.
    """
    cleaned_docs: List[Document] = []
    for doc in docs:
        page_content = doc.page_content.strip()
        # Filter out completely blank or noise pages
        if not page_content or len(page_content) < 40:
            continue

        source = doc.metadata.get("source", "Medical_book.pdf")
        page = doc.metadata.get("page", 0)

        cleaned_docs.append(
            Document(
                page_content=page_content,
                metadata={
                    "source": os.path.basename(source),
                    "page": page + 1  # 1-indexed human readable page
                }
            )
        )
    return cleaned_docs


def chunk_documents(
    docs: List[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 150
) -> List[Document]:
    """
    Splits long documents into semantically coherent overlapping chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunked = splitter.split_documents(docs)
    print(f"Created {len(chunked)} text chunks from {len(docs)} pages.")
    return chunked


def download_embedding(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    """Create the configured embedding client for indexing and retrieval."""
    provider = os.getenv("EMBEDDING_PROVIDER", "local").strip().lower()

    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is required when EMBEDDING_PROVIDER=gemini."
            )

        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        return GoogleGenerativeAIEmbeddings(
            model=os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001"),
            google_api_key=api_key,
        )

    if provider != "local":
        raise ValueError(
            f"Unsupported EMBEDDING_PROVIDER '{provider}'. Use 'local' or 'gemini'."
        )

    try:
        from langchain_huggingface import HuggingFaceEmbeddings
    except ImportError:
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings
        except ImportError as error:
            raise RuntimeError(
                "Local embeddings require the 'langchain-huggingface' package."
            ) from error

    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )