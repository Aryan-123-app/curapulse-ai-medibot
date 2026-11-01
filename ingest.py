"""
Automated Data Ingestion Pipeline for CuraPulse AI.
Extracts medical reference data from PDFs, generates vector embeddings,
and stores them in ChromaDB (local) or Pinecone (cloud).

Usage:
    python ingest.py --store chroma
    python ingest.py --store pinecone
    python ingest.py --store chroma --limit 100    # quick test with first 100 pages
"""

import os
import argparse
import sys
from dotenv import load_dotenv
from src.helper import load_pdf_documents, filter_and_clean_docs, chunk_documents, download_embedding

load_dotenv()


def ingest_to_chroma(chunks, embeddings, persist_dir: str = "vectorstore"):
    """Indexes chunks into a local persistent Chroma database."""
    try:
        from langchain_chroma import Chroma
    except ImportError:
        try:
            from langchain_community.vectorstores import Chroma
        except ImportError:
            print("Error: 'chromadb' or 'langchain-chroma' is not installed.")
            print("Run: pip install langchain-chroma chromadb")
            sys.exit(1)

    print(f"\n[1/2] Initializing local Chroma vector store at '{persist_dir}'...")
    os.makedirs(persist_dir, exist_ok=True)

    # Process in batches to handle large documents comfortably
    batch_size = 500
    total_chunks = len(chunks)
    vector_store = None

    for i in range(0, total_chunks, batch_size):
        batch = chunks[i : i + batch_size]
        print(f"  Indexing batch {i // batch_size + 1}/{(total_chunks + batch_size - 1) // batch_size} ({len(batch)} chunks)...")
        if vector_store is None:
            vector_store = Chroma.from_documents(
                documents=batch,
                embedding=embeddings,
                persist_directory=persist_dir
            )
        else:
            vector_store.add_documents(documents=batch)

    print(f"\n[2/2] Successfully indexed {total_chunks} chunks into local ChromaDB at '{persist_dir}'.")
    return vector_store


def ingest_to_pinecone(chunks, embeddings, index_name: str = "curapulse-medical"):
    """Indexes chunks into a Pinecone cloud vector database."""
    api_key = os.getenv("PINECONE_API_KEY", "").strip()
    if not api_key:
        print("Error: PINECONE_API_KEY environment variable is missing in .env.")
        sys.exit(1)

    try:
        from pinecone import Pinecone, ServerlessSpec
        from langchain_pinecone import PineconeVectorStore
    except ImportError:
        print("Error: 'pinecone' or 'langchain-pinecone' is not installed.")
        print("Run: pip install pinecone langchain-pinecone")
        sys.exit(1)

    pc = Pinecone(api_key=api_key)
    existing_indexes = [idx["name"] for idx in pc.list_indexes()]

    # all-MiniLM-L6-v2 produces 384-dimensional embeddings
    dimension = 384
    if index_name not in existing_indexes:
        print(f"Creating new Pinecone Serverless index '{index_name}' (dimension={dimension})...")
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print(f"Index '{index_name}' created successfully.")
    else:
        print(f"Using existing Pinecone index: '{index_name}'")

    print(f"Uploading {len(chunks)} chunks to Pinecone index '{index_name}'...")
    batch_size = 100
    total_chunks = len(chunks)

    for i in range(0, total_chunks, batch_size):
        batch = chunks[i : i + batch_size]
        print(f"  Upserting batch {i // batch_size + 1}/{(total_chunks + batch_size - 1) // batch_size}...")
        PineconeVectorStore.from_documents(
            documents=batch,
            embedding=embeddings,
            index_name=index_name
        )

    print(f"\nSuccessfully indexed {total_chunks} chunks into Pinecone '{index_name}'.")


def main():
    parser = argparse.ArgumentParser(description="CuraPulse AI Data Ingestion Pipeline")
    parser.add_argument(
        "--store",
        type=str,
        choices=["chroma", "pinecone"],
        default=os.getenv("VECTOR_STORE_TYPE", "chroma"),
        help="Vector database destination ('chroma' for local, 'pinecone' for cloud)"
    )
    parser.add_argument(
        "--data",
        type=str,
        default="data",
        help="Directory containing source PDF files (default: 'data')"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit the number of PDF pages to process (useful for rapid testing)"
    )
    parser.add_argument(
        "--index-name",
        type=str,
        default=os.getenv("PINECONE_INDEX_NAME", "curapulse-medical"),
        help="Pinecone index name (default: 'curapulse-medical')"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("      CuraPulse AI - Medical Knowledge Ingestion Pipeline")
    print("=" * 60)
    print(f"Source Directory : {args.data}")
    print(f"Target Store     : {args.store}")

    # 1. Load documents
    docs = load_pdf_documents(args.data, limit=args.limit)


    # 2. Filter & Clean
    cleaned_docs = filter_and_clean_docs(docs)

    # 3. Chunk documents
    chunks = chunk_documents(cleaned_docs, chunk_size=1000, chunk_overlap=150)

    # 4. Initialize embedding model
    print("\nLoading embedding model (sentence-transformers/all-MiniLM-L6-v2)...")
    embeddings = download_embedding()

    # 5. Store embeddings
    if args.store == "chroma":
        ingest_to_chroma(chunks, embeddings, persist_dir="vectorstore")
    elif args.store == "pinecone":
        ingest_to_pinecone(chunks, embeddings, index_name=args.index_name)

    print("\nIngestion complete! You can now launch the web assistant with:")
    print("  streamlit run app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
