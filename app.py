"""
CuraPulse AI - Intelligent Medical Knowledge Retrieval & Healthcare Assistant
Built with LangChain, Google Gemini, HuggingFace Embeddings, and ChromaDB / Pinecone.

Author: Aryan Patade
"""

import os
import sys
import streamlit as st
from dotenv import load_dotenv

# Load local environment variables from .env if present
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="CuraPulse AI | Clinical Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern clinical aesthetics
st.markdown("""
<style>
    /* Main container styling */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header hero styling */
    .hero-banner {
        background: linear-gradient(135deg, #0d324d 0%, #175676 50%, #4ba3c3 100%);
        padding: 1.8rem 2rem;
        border-radius: 14px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.9;
        margin-top: 6px;
        margin-bottom: 0;
    }
    
    /* Disclaimer alert */
    .disclaimer-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        color: #856404;
        padding: 0.85rem 1.2rem;
        border-radius: 6px;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }
    
    /* Source chip cards */
    .source-card {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
    }
    .source-title {
        font-weight: 600;
        color: #175676;
    }
    
    /* Quick prompt button styling */
    div[data-testid="stHorizontalBlock"] button {
        border-radius: 20px;
        font-size: 0.82rem;
    }
</style>
""", unsafe_allow_html=True)


def get_secret(key: str, default: str = "") -> str:
    """Helper to retrieve credentials from st.secrets or os.environ."""
    val = default
    if key in os.environ and os.environ[key]:
        val = os.environ[key]
    else:
        try:
            if key in st.secrets:
                val = st.secrets[key]
        except Exception:
            pass
    return str(val).strip() if val else default



# Retrieve credentials
GEMINI_API_KEY = get_secret("GEMINI_API_KEY")
PINECONE_API_KEY = get_secret("PINECONE_API_KEY")
PINECONE_INDEX_NAME = get_secret("PINECONE_INDEX_NAME", "curapulse-medical")
VECTOR_STORE_TYPE = get_secret("VECTOR_STORE_TYPE", "chroma").lower()


# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/caduceus.png", width=64)
    st.title("CuraPulse AI")
    st.caption("Grounded Healthcare RAG System")
    st.markdown("---")
    
    st.subheader("⚙️ System Status")
    
    # Vector store selector
    vector_mode = st.radio(
        "Vector Database",
        options=["ChromaDB (Local)", "Pinecone (Cloud)"],
        index=0 if VECTOR_STORE_TYPE == "chroma" else 1,
        help="Choose between offline local ChromaDB or cloud-hosted Pinecone vector store."
    )
    selected_store = "chroma" if "Chroma" in vector_mode else "pinecone"
    
    # Top-K retrieval slider
    retrieval_k = st.slider(
        "Context Chunks (k)",
        min_value=2,
        max_value=8,
        value=4,
        help="Number of medical book excerpts to retrieve per query."
    )
    
    # Model selection
    gemini_model_choice = st.selectbox(
        "Gemini Model",
        options=["gemini-2.5-flash-lite", "gemini-3.5-flash", "gemini-3-flash-preview"],
        index=0
    )

    
    st.markdown("---")
    
    # Knowledge base metadata
    st.subheader("📚 Knowledge Base")
    st.markdown("""
    - **Source**: *The Gale Encyclopedia of Medicine*
    - **Scope**: 1,700+ medical disorders, conditions, tests & therapies
    - **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
    """)
    
    st.markdown("---")
    
    if st.button("🧹 Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    st.caption("Developed by **Aryan Patade** • [GitHub Repository](https://github.com/Aryan-123-app/CuraPulse-AI)")


# Hero banner
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🩺 CuraPulse AI</div>
    <div class="hero-subtitle">Intelligent, grounded medical knowledge assistant powered by verified clinical literature and Retrieval-Augmented Generation.</div>
</div>
""", unsafe_allow_html=True)

# Medical disclaimer alert
st.markdown("""
<div class="disclaimer-box">
    <strong>⚠️ Medical Disclaimer:</strong> CuraPulse AI is designed strictly for informational and educational purposes. It is grounded in <em>The Gale Encyclopedia of Medicine</em>, but is <strong>not</strong> a substitute for professional clinical advice, diagnosis, or treatment. If you are experiencing a medical emergency, call your local emergency services (<strong>911 / 112</strong>) immediately.
</div>
""", unsafe_allow_html=True)


# Validation for Gemini Key
if not GEMINI_API_KEY:
    st.error("⚠️ **Missing GEMINI_API_KEY**: Please add your Gemini API key to `.env` or Streamlit Secrets.")
    st.info("You can obtain a free Gemini API key at [Google AI Studio](https://aistudio.google.com/app/apikey).")
    st.stop()


# Cached vector store loader to avoid reloading embeddings on every turn
@st.cache_resource(show_spinner=False)
def load_retriever(store_type: str, k: int):
    """Loads the vector retriever from ChromaDB or Pinecone."""
    from src.helper import download_embedding
    embeddings = download_embedding()
    
    if store_type == "chroma":
        persist_dir = "vectorstore"
        if not os.path.exists(persist_dir) or not os.listdir(persist_dir):
            return None, "Chroma vector store not found locally. Please run: `python ingest.py --store chroma` first."
        
        try:
            from langchain_chroma import Chroma
        except ImportError:
            from langchain_community.vectorstores import Chroma
            
        vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings
        )
        return vectorstore.as_retriever(search_kwargs={"k": k}), None

    else:
        # Pinecone
        if not PINECONE_API_KEY:
            return None, "PINECONE_API_KEY is not configured in .env or Streamlit Secrets."
        
        try:
            from pinecone import Pinecone
            from langchain_pinecone import PineconeVectorStore
        except ImportError:
            return None, "Dependencies for Pinecone not found. Install with: pip install pinecone langchain-pinecone"
            
        pc = Pinecone(api_key=PINECONE_API_KEY)
        vectorstore = PineconeVectorStore.from_existing_index(
            index_name=PINECONE_INDEX_NAME,
            embedding=embeddings
        )
        return vectorstore.as_retriever(search_kwargs={"k": k}), None


# Initialize session state for messages and conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am **CuraPulse AI**, your medical knowledge assistant. Ask me anything regarding clinical conditions, symptoms, medical tests, or treatments referenced in medical literature.",
            "sources": []
        }
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Initialize Retriever
retriever, error_msg = load_retriever(selected_store, retrieval_k)

if error_msg:
    st.warning(f"⚠️ {error_msg}")
    st.info("💡 **Quick Start**: You can generate your local vector database right away by running:\n```bash\npython ingest.py --store chroma --limit 50\n```")


# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🩺" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📚 Verified Clinical Citations"):
                for idx, src in enumerate(msg["sources"], 1):
                    st.markdown(
                        f"**[{idx}] {src.get('source', 'Medical Reference')}** — *Page {src.get('page', 'N/A')}*\n"
                        f"> {src.get('excerpt', '')}"
                    )


# Quick prompt starter suggestions
if len(st.session_state.messages) <= 1:
    st.markdown("##### 💡 Suggested Inquiries:")
    col1, col2, col3 = st.columns(3)
    quick_query = None
    if col1.button("🫀 What causes an Abdominal Aortic Aneurysm?", use_container_width=True):
        quick_query = "What causes an Abdominal Aortic Aneurysm, and what are its symptoms and diagnosis?"
    if col2.button("🫁 What are common Asthma symptoms & triggers?", use_container_width=True):
        quick_query = "What are the common symptoms, triggers, and medical management of Asthma?"
    if col3.button("🩸 How is Diabetes Mellitus diagnosed?", use_container_width=True):
        quick_query = "What diagnostic tests are used for Diabetes Mellitus and what are key precautions?"
else:
    quick_query = None


# Handle user input from chat input or quick prompt
user_prompt = st.chat_input("Ask a clinical or healthcare question...") or quick_query

if user_prompt:
    if not retriever:
        st.error("Vector database is not ready. Please ingest documents before asking questions.")
        st.stop()

    # Append user prompt to UI
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_prompt)

    # Generate assistant response
    with st.chat_message("assistant", avatar="🩺"):
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
        try:
            from langchain.chains import create_history_aware_retriever, create_retrieval_chain
            from langchain.chains.combine_documents import create_stuff_documents_chain
        except ImportError:
            from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
            from langchain_classic.chains.combine_documents import create_stuff_documents_chain
        from src.prompt import SYSTEM_PROMPT, CONTEXTUALIZE_Q_SYSTEM_PROMPT


        llm = ChatGoogleGenerativeAI(
            model=gemini_model_choice,
            google_api_key=GEMINI_API_KEY,
            temperature=0.2,
            streaming=True
        )

        # Contextualize question based on history
        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", CONTEXTUALIZE_Q_SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_q_prompt
        )

        # Answer question prompt
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        with st.spinner("Analyzing medical literature..."):
            try:
                response = rag_chain.invoke({
                    "input": user_prompt,
                    "chat_history": st.session_state.chat_history
                })
                answer = response.get("answer", "")
                context_docs = response.get("context", [])
                
                # Format sources
                sources = []
                for doc in context_docs:
                    sources.append({
                        "source": doc.metadata.get("source", "Medical Reference Book"),
                        "page": doc.metadata.get("page", "Unknown"),
                        "excerpt": doc.page_content[:240].replace("\n", " ") + "..."
                    })

                # Stream answer to UI
                st.markdown(answer)

                if sources:
                    with st.expander("📚 Verified Clinical Citations"):
                        for idx, src in enumerate(sources, 1):
                            st.markdown(
                                f"**[{idx}] {src['source']}** — *Page {src['page']}*\n"
                                f"> {src['excerpt']}"
                            )

                # Update session states
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
                st.session_state.chat_history.extend([
                    ("human", user_prompt),
                    ("assistant", answer)
                ])

            except Exception as e:
                st.error(f"Error generating clinical response: {str(e)}")
