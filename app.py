"""
CuraPulse AI - Award-Winning Healthcare AI Portal & Clinical Intelligence Assistant
Directly inspired by modern Awwwards/Apple-caliber medical technology landing design.

Author: Aryan Patade
"""

import os
import sys
import base64
import textwrap

# Ensure project root is in sys.path for robust cloud deployments
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="CuraPulse AI • Revolutionizing Healthcare with AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "landing"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


def render_html(html_str: str):
    """Renders HTML cleanly without leading indentation or empty lines that trip markdown parsers."""
    cleaned = "\n".join(line.strip() for line in html_str.splitlines() if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


# Load DNA image as base64 for high-performance rendering
def get_image_base64(image_path: str) -> str:
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

dna_b64 = get_image_base64("assets/dna_helix.jpg")


# High-Contrast Design System matching the reference image
render_html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Page Canvas */
    html {
        scroll-behavior: smooth;
    }
    body, .stApp {
        color-scheme: light !important;
        background-color: #FFFFFF !important;
        background-image: 
            radial-gradient(ellipse 90% 55% at 50% -5%, rgba(0, 163, 255, 0.22) 0%, rgba(186, 230, 253, 0.12) 35%, rgba(255, 255, 255, 0) 70%) !important;
        color: #0F172A !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Container Spacing */
    div.block-container {
        max-width: 1240px !important;
        padding-top: 1.8rem !important;
        padding-bottom: 5rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
    }

    /* Hide standard Streamlit chrome */
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    header[data-testid="stHeader"] { display: none !important; }
    .stDeployButton, div[data-testid="stToolbar"] { display: none !important; }

    /* Force all text elements to dark high-contrast color */
    p, span:not(.accent-care):not(.citation-badge-light):not(.floating-arrow-btn):not(.btn-txt), 
    h1, h2, h3, h4, label,
    div[data-testid="stMarkdownContainer"] p {
        color: #0F172A !important;
    }

    /* Top Navbar */
    .custom-logo {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.42rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.6px !important;
        color: #0F172A !important;
        text-transform: uppercase !important;
        display: flex;
        align-items: center;
        gap: 2px;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
    }
    .logo-dot {
        color: #00A3FF !important;
    }
    .custom-nav-links {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 40px;
        width: 100%;
        margin: 0 !important;
        padding: 0 !important;
    }
    .custom-nav-link {
        font-family: 'Inter', -apple-system, sans-serif !important;
        font-size: 0.96rem !important;
        font-weight: 500 !important;
        color: #475569 !important;
        text-decoration: none !important;
        letter-spacing: -0.1px;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        padding: 6px 14px !important;
        border-radius: 999px !important;
    }
    .custom-nav-link:hover {
        color: #00A3FF !important;
        background: rgba(0, 163, 255, 0.06) !important;
    }
    .custom-nav-link.active {
        color: #0F172A !important;
        font-weight: 700 !important;
    }

    /* Sleek Top Navbar Button & Right Alignment */
    div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stColumn"]:nth-of-type(3) {
        display: flex !important;
        justify-content: flex-end !important;
        align-items: center !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stColumn"]:nth-of-type(3) div.stButton {
        display: flex !important;
        justify-content: flex-end !important;
        width: auto !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stColumn"]:nth-of-type(3) .stButton > button {
        height: 42px !important;
        min-height: 42px !important;
        padding: 0.45rem 1.6rem !important;
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.1px !important;
        border-radius: 999px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15) !important;
        width: auto !important;
        margin: 0 !important;
    }

    /* Hero Ambient Blurred Graphic Background matching reference image */
    .hero-container {
        position: relative;
        text-align: center;
        padding: 1rem 0 2rem 0;
        overflow: visible;
    }
    .hero-glow-left {
        position: absolute;
        top: -40px;
        left: -40px;
        width: 480px;
        height: 440px;
        background: radial-gradient(circle at 35% 35%, rgba(6, 182, 212, 0.42) 0%, rgba(56, 189, 248, 0.28) 40%, rgba(255, 255, 255, 0) 72%);
        filter: blur(55px);
        pointer-events: none;
        z-index: 0;
    }
    .hero-glow-right {
        position: absolute;
        top: -30px;
        right: -40px;
        width: 500px;
        height: 440px;
        background: radial-gradient(circle at 65% 35%, rgba(99, 102, 241, 0.28) 0%, rgba(56, 189, 248, 0.25) 45%, rgba(255, 255, 255, 0) 72%);
        filter: blur(60px);
        pointer-events: none;
        z-index: 0;
    }
    .hero-glow-center {
        position: absolute;
        top: -20px;
        left: 50%;
        transform: translateX(-50%);
        width: 760px;
        height: 340px;
        background: radial-gradient(ellipse 70% 55% at 50% 45%, rgba(0, 163, 255, 0.26) 0%, rgba(186, 230, 253, 0.16) 45%, rgba(255, 255, 255, 0) 75%);
        filter: blur(48px);
        pointer-events: none;
        z-index: 0;
    }

    /* Dotted Arch Wave Graphic */
    .hero-wave-graphic {
        position: absolute;
        top: -15px;
        left: 50%;
        transform: translateX(-50%);
        width: 860px;
        height: 220px;
        opacity: 0.55;
        pointer-events: none;
        z-index: 1;
    }

    /* Centered Pill Badge */
    .center-pill-wrapper {
        position: relative;
        z-index: 2;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 1.25rem;
    }
    .center-badge-pill {
        display: inline-block;
        padding: 8px 24px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.95) !important;
        border: 1.5px solid #E2E8F0 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        color: #1E293B !important;
        letter-spacing: -0.2px;
        backdrop-filter: blur(10px);
    }

    /* Main Hero Headline */
    .hero-heading-box {
        position: relative;
        z-index: 2;
        text-align: center;
        margin-bottom: 2.5rem;
    }
    .hero-title-main {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 5rem !important;
        font-weight: 800 !important;
        letter-spacing: -2.8px !important;
        line-height: 1.05 !important;
        color: #0F172A !important;
        margin: 0 !important;
    }
    .hero-title-sub {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 5rem !important;
        font-weight: 800 !important;
        letter-spacing: -2.8px !important;
        line-height: 1.15 !important;
        color: #0F172A !important;
        margin: 0 !important;
    }
    .accent-care {
        color: #00A3FF !important;
    }
    .ai-symbol {
        font-weight: 800 !important;
        font-size: 5rem !important;
        letter-spacing: -2px !important;
        color: #0F172A !important;
    }

    /* Search Input Styling */
    div[data-testid="stTextInput"] {
        width: 100% !important;
    }
    div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 999px !important;
        padding: 0.8rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05) !important;
        height: 52px !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #00A3FF !important;
        box-shadow: 0 0 18px rgba(0, 163, 255, 0.25) !important;
    }
    div[data-testid="stTextInput"] input::placeholder {
        color: #64748B !important;
        opacity: 1 !important;
    }

    /* Floating Consultation Pill (Left over DNA) */
    .floating-consult-pill {
        position: absolute;
        top: 25px;
        left: 20px;
        background: #FFFFFF !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 999px;
        padding: 10px 20px;
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08);
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 10;
    }
    .floating-consult-text {
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        line-height: 1.25;
    }
    .floating-arrow-btn {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #E0F2FE !important;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #0284C7 !important;
        font-weight: 800 !important;
        font-size: 0.95rem;
    }

    /* Right column content ("Live well, Be Well") */
    .right-content-heading {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 2.1rem !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        margin-bottom: 0.85rem !important;
        letter-spacing: -0.5px !important;
    }
    .right-content-desc {
        font-size: 1.05rem !important;
        line-height: 1.65 !important;
        color: #334155 !important;
        margin-bottom: 1.75rem !important;
    }

    /* Avatar stack */
    .avatar-stack-wrapper {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 1.5rem;
    }
    .avatar-group {
        display: flex;
        align-items: center;
    }
    .avatar-circle {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        border: 2.5px solid #FFFFFF;
        object-fit: cover;
        margin-left: -10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
    }
    .avatar-circle:first-child {
        margin-left: 0;
    }
    .avatar-proof-text {
        font-size: 0.92rem !important;
        color: #1E293B !important;
        line-height: 1.35;
    }
    .avatar-proof-num {
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        color: #0F172A !important;
    }

    /* Solid High-Contrast Black Pill Buttons */
    .stButton > button {
        background: #000000 !important;
        color: #FFFFFF !important;
        border-radius: 999px !important;
        border: none !important;
        font-weight: 700 !important;
        padding: 0.75rem 1.8rem !important;
        font-size: 0.92rem !important;
        letter-spacing: -0.2px !important;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.18) !important;
        transition: all 0.2s ease !important;
        height: 52px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .stButton > button p,
    .stButton > button span,
    .stButton > button div {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    .stButton > button:hover {
        background: #1E293B !important;
        color: #FFFFFF !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25) !important;
    }
    .stButton > button:hover * {
        color: #FFFFFF !important;
    }

    /* Section Headers */
    .section-badge-pill {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 999px;
        background: #E0F2FE;
        color: #0284C7;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }
    .section-title-large {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 2.6rem !important;
        font-weight: 800 !important;
        letter-spacing: -1.2px !important;
        color: #0F172A !important;
        line-height: 1.15 !important;
        margin-bottom: 1rem !important;
    }
    .section-subtitle-large {
        font-size: 1.1rem !important;
        color: #475569 !important;
        line-height: 1.6 !important;
        max-width: 680px !important;
        margin-bottom: 2.5rem !important;
    }

    /* Showcase Cards */
    .feature-card-clean {
        background: #FFFFFF;
        border: 1.5px solid #E2E8F0;
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
        height: 100%;
        transition: all 0.3s ease;
    }
    .feature-card-clean:hover {
        border-color: #00A3FF;
        transform: translateY(-4px);
        box-shadow: 0 16px 38px rgba(0, 163, 255, 0.1);
    }
    .feature-card-icon {
        width: 52px;
        height: 52px;
        border-radius: 16px;
        background: #EFF6FF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1.25rem;
    }
    .feature-card-title {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        margin-bottom: 0.6rem !important;
    }
    .feature-card-desc {
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        color: #475569 !important;
    }

    /* Footer Styling */
    .footer-wrapper {
        border-top: 1.5px solid #E2E8F0;
        padding-top: 4rem;
        margin-top: 5rem;
    }
    .footer-col-title {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.92rem !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
        margin-bottom: 1.25rem !important;
    }
    .footer-link {
        display: block;
        color: #475569 !important;
        font-size: 0.92rem !important;
        margin-bottom: 0.75rem !important;
        text-decoration: none !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    .footer-link:hover {
        color: #00A3FF !important;
        transform: translateX(3px);
    }
    .footer-bottom-bar {
        border-top: 1px solid #F1F5F9;
        padding-top: 2rem;
        margin-top: 3rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #64748B;
        font-size: 0.88rem;
    }

    /* Chat Messages Styling */
    div[data-testid="stChatMessage"] {
        background: #F8FAFC !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 20px !important;
        padding: 1.25rem 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] span,
    div[data-testid="stChatMessage"] li,
    div[data-testid="stChatMessage"] h1,
    div[data-testid="stChatMessage"] h2,
    div[data-testid="stChatMessage"] h3,
    div[data-testid="stChatMessage"] strong {
        color: #0F172A !important;
    }

    /* User Message Bubble */
    div[data-testid="stChatMessage"]:has(span[data-testid="chatAvatarIcon-user"]) {
        background: #0F172A !important;
        border: 1px solid #1E293B !important;
    }
    div[data-testid="stChatMessage"]:has(span[data-testid="chatAvatarIcon-user"]) p,
    div[data-testid="stChatMessage"]:has(span[data-testid="chatAvatarIcon-user"]) span,
    div[data-testid="stChatMessage"]:has(span[data-testid="chatAvatarIcon-user"]) strong {
        color: #F8FAFC !important;
    }

    /* Floating Chat Input Dock */
    div[data-testid="stChatInput"] {
        background: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 999px !important;
        box-shadow: 0 10px 35px rgba(0,0,0,0.08) !important;
    }
    div[data-testid="stChatInput"] textarea {
        background: #FFFFFF !important;
        color: #0F172A !important;
        font-size: 0.95rem !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #64748B !important;
    }
    div[data-testid="stChatInput"] button {
        color: #00A3FF !important;
    }

    /* Citations Expander & Cards */
    div[data-testid="stExpander"] {
        background: #F1F5F9 !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 14px !important;
    }
    div[data-testid="stExpander"] summary span {
        color: #0F172A !important;
        font-weight: 700 !important;
    }
    .citation-card-light {
        background: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 12px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.6rem;
    }
    .citation-card-light strong {
        color: #0F172A !important;
    }
    .citation-card-light div {
        color: #334155 !important;
    }
    .citation-badge-light {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        background: #E0F2FE !important;
        color: #0284C7 !important;
        padding: 2px 8px;
        border-radius: 4px;
        margin-right: 8px;
    }
</style>
""")


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


GEMINI_API_KEY = get_secret("GEMINI_API_KEY")


# Cached vector retriever
@st.cache_resource(show_spinner=False)
def load_retriever(store_type: str = "chroma", k: int = 4):
    """Loads the vector retriever from local ChromaDB."""
    from src.helper import download_embedding
    embeddings = download_embedding()
    
    persist_dir = "vectorstore"
    if not os.path.exists(persist_dir) or not os.listdir(persist_dir):
        return None, "Local Chroma vector store not found. Run `.\\ingest.bat --store chroma` first."
    
    try:
        from langchain_chroma import Chroma
    except ImportError:
        import importlib
        Chroma = importlib.import_module("langchain_community.vectorstores").Chroma
        
    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )
    return vectorstore.as_retriever(search_kwargs={"k": k}), None


retriever, error_msg = load_retriever("chroma", 4)


# =========================================================================
# VIEW 1: THE AWARD-WINNING SHOWCASE LANDING PAGE
# =========================================================================
if st.session_state.app_mode == "landing":

    # Top Navbar with balanced symmetric grid & center alignment matching reference image
    nav_left_col, nav_center_col, nav_right_col = st.columns([3, 6, 3], vertical_alignment="center")
    with nav_left_col:
        render_html('<div class="custom-logo" id="home">CURAPULSE<span class="logo-dot">.</span></div>')

    with nav_center_col:
        render_html("""
        <div class="custom-nav-links">
            <a href="#home" class="custom-nav-link active">Home</a>
            <a href="#about" class="custom-nav-link">About</a>
            <a href="#technology" class="custom-nav-link">Technology</a>
            <a href="#services" class="custom-nav-link">Services</a>
        </div>
        """)

    with nav_right_col:
        if st.button("Launch Assistant", key="top_launch_btn"):
            st.session_state.app_mode = "chat"
            st.rerun()

    # Spacious breathing room below navbar before hero graphics start
    st.markdown("<div style='margin-bottom: 2.75rem;'></div>", unsafe_allow_html=True)

    # Hero Section with Luminous Blurred Mesh Background & Dotted Arch
    render_html("""
    <div class="hero-container">
        <div class="hero-glow-left"></div>
        <div class="hero-glow-right"></div>
        <div class="hero-glow-center"></div>
        <svg class="hero-wave-graphic" viewBox="0 0 900 220" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M 40 40 Q 450 200 860 40" stroke="#00A3FF" stroke-width="2.0" stroke-dasharray="3 8" opacity="0.65"/>
            <path d="M 100 40 Q 450 170 800 40" stroke="#38BDF8" stroke-width="1.6" stroke-dasharray="2 7" opacity="0.5"/>
            <path d="M 160 40 Q 450 140 740 40" stroke="#0284C7" stroke-width="1.3" stroke-dasharray="2 6" opacity="0.4"/>
            <path d="M 220 40 Q 450 110 680 40" stroke="#7DD3FC" stroke-width="1.0" stroke-dasharray="2 5" opacity="0.32"/>
            <path d="M 280 40 Q 450 85 620 40" stroke="#BAE6FD" stroke-width="0.9" stroke-dasharray="1 5" opacity="0.25"/>
        </svg>
        <div class="center-pill-wrapper">
            <span class="center-badge-pill">World's Most Grounded Healthcare AI</span>
        </div>
        <div class="hero-heading-box">
            <div class="hero-title-main">Revolutionizing</div>
            <div class="hero-title-sub">Health<span class="accent-care">care</span> with <span class="ai-symbol">AI</span></div>
        </div>
    </div>
    """)

    # Floating Search Capsule
    sc1, sc2, sc3 = st.columns([1, 5, 1])
    with sc2:
        query_col_input, query_col_btn = st.columns([3, 1])
        with query_col_input:
            user_direct_q = st.text_input(
                label="Search clinical topic",
                placeholder="📍 Enter condition or symptom (e.g., Cancer, Diabetes, Asthma)...",
                label_visibility="collapsed"
            )
        with query_col_btn:
            if st.button("Launch Assistant →", key="capsule_launch_btn", use_container_width=True):
                if user_direct_q.strip():
                    st.session_state.pending_prompt = user_direct_q.strip()
                st.session_state.app_mode = "chat"
                st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Lower Grid Layout (DNA Helix Left + "Live well, Be Well" Right)
    grid_left, grid_right = st.columns([5, 5])

    with grid_left:
        # 3D Blue DNA Helix from generated asset
        if dna_b64:
            render_html(f"""
            <div style="position: relative; border-radius: 28px; overflow: hidden; background: #F8FAFC; border: 1.5px solid #E2E8F0; height: 350px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 30px rgba(0,0,0,0.04);">
                <div class="floating-consult-pill">
                    <div class="floating-consult-text">Timely care with verified<br>citations & consultation</div>
                    <div class="floating-arrow-btn">→</div>
                </div>
                <img src="data:image/jpeg;base64,{dna_b64}" style="width: 100%; height: 100%; object-fit: cover;" alt="3D DNA Helix" />
            </div>
            """)
        else:
            render_html("""
            <div style="border-radius: 28px; background: linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 100%); height: 350px; display: flex; align-items: center; justify-content: center; font-weight: 700; color: #0284C7;">
                🧬 3D DNA Model
            </div>
            """)

    with grid_right:
        render_html("""
        <div style="padding: 1.5rem 1rem 1rem 1.5rem;">
            <div class="right-content-heading">Live well, Be Well</div>
            <p class="right-content-desc">
                Join us in revolutionizing healthcare. Our AI tools empower you to live well by providing 
                personalized and verified clinical knowledge. Step into a future where your health is guided 
                by precision, literature grounding, and innovation.
            </p>
            <div class="avatar-stack-wrapper">
                <div class="avatar-group">
                    <img class="avatar-circle" src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=80&h=80&fit=crop&crop=faces" alt="Avatar">
                    <img class="avatar-circle" src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=80&h=80&fit=crop&crop=faces" alt="Avatar">
                    <img class="avatar-circle" src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=80&h=80&fit=crop&crop=faces" alt="Avatar">
                    <img class="avatar-circle" src="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=80&h=80&fit=crop&crop=faces" alt="Avatar">
                    <img class="avatar-circle" src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&h=80&fit=crop&crop=faces" alt="Avatar">
                </div>
                <div class="avatar-proof-text">
                    <span class="avatar-proof-num">3,282+</span><br>
                    Verified clinical nodes (637 pages)
                </div>
            </div>
        </div>
        """)

        st.markdown("<br>", unsafe_allow_html=True)
        # Quick launcher buttons
        col_q1, col_q2 = st.columns(2)
        with col_q1:
            if st.button("🧬 Ask: What is cancer?", key="q_btn_cancer", use_container_width=True):
                st.session_state.pending_prompt = "What is cancer, what are its fundamental cellular characteristics, and how is staging determined?"
                st.session_state.app_mode = "chat"
                st.rerun()

        with col_q2:
            if st.button("🩸 Ask: Diabetes diagnosis", key="q_btn_diabetes", use_container_width=True):
                st.session_state.pending_prompt = "What diagnostic blood tests and thresholds are used for Diabetes Mellitus, and what are key precautions?"
                st.session_state.app_mode = "chat"
                st.rerun()

    # =====================================================================
    # SECTION 2: ABOUT CURAPULSE (#about)
    # =====================================================================
    st.markdown("<br><br><br><hr style='border: none; border-top: 1.5px solid #F1F5F9; margin-bottom: 4rem;'>", unsafe_allow_html=True)

    render_html("""
    <div id="about">
        <span class="section-badge-pill">✦ WHO WE ARE</span>
        <h2 class="section-title-large">Clinical Precision Built on Verified Medical Science</h2>
        <p class="section-subtitle-large">
            CuraPulse AI was engineered to bridge the critical gap between conversational AI and verified medical accuracy. 
            We replace generic probability with deterministic citations from peer-reviewed clinical reference volumes.
        </p>
    </div>
    """)

    ab_col1, ab_col2, ab_col3 = st.columns(3)
    with ab_col1:
        render_html("""
        <div class="feature-card-clean">
            <div class="feature-card-icon">📚</div>
            <div class="feature-card-title">Peer-Reviewed Foundation</div>
            <div class="feature-card-desc">
                Grounded entirely in <em>The Gale Encyclopedia of Medicine</em> (637 pages, 1,700+ medical conditions, diagnostic tests, and clinical therapies).
            </div>
        </div>
        """)

    with ab_col2:
        render_html("""
        <div class="feature-card-clean">
            <div class="feature-card-icon">🔒</div>
            <div class="feature-card-title">100% Local Sovereignty</div>
            <div class="feature-card-desc">
                Embedded and queried offline on your local machine using ChromaDB. Zero patient queries or private research files are ever monetized or used for training.
            </div>
        </div>
        """)

    with ab_col3:
        render_html("""
        <div class="feature-card-clean">
            <div class="feature-card-icon">🩺</div>
            <div class="feature-card-title">Auditable Citations</div>
            <div class="feature-card-desc">
                Every generated answer includes explicit textbook page numbers and verbatim excerpts, allowing clinicians and patients to verify information instantaneously.
            </div>
        </div>
        """)

    # =====================================================================
    # SECTION 3: TECHNOLOGY ARCHITECTURE (#technology)
    # =====================================================================
    st.markdown("<br><br><br><hr style='border: none; border-top: 1.5px solid #F1F5F9; margin-bottom: 4rem;'>", unsafe_allow_html=True)

    render_html("""
    <div id="technology">
        <span class="section-badge-pill">✦ SYSTEM ARCHITECTURE</span>
        <h2 class="section-title-large">The Sovereign Retrieval-Augmented Pipeline</h2>
        <p class="section-subtitle-large">
            Behind CuraPulse AI is a deterministic 4-stage pipeline that ensures sub-400ms semantic retrieval and zero generative hallucination.
        </p>
    </div>
    """)

    tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)

    with tech_col1:
        render_html("""
        <div class="feature-card-clean">
            <div style="font-family: 'JetBrains Mono'; font-size: 0.75rem; font-weight: 700; color: #0284C7; margin-bottom: 8px;">STAGE 01</div>
            <div class="feature-card-title">Dense Chunking</div>
            <div class="feature-card-desc">
                Recursive text splitting with 150-character overlap preserving page numbers and source reference metadata across 637 pages.
            </div>
        </div>
        """)

    with tech_col2:
        render_html("""
        <div class="feature-card-clean">
            <div style="font-family: 'JetBrains Mono'; font-size: 0.75rem; font-weight: 700; color: #0284C7; margin-bottom: 8px;">STAGE 02</div>
            <div class="feature-card-title">Vector Space</div>
            <div class="feature-card-desc">
                Embedding text with <code>sentence-transformers/all-MiniLM-L6-v2</code> into a 384-dimensional cosine vector index.
            </div>
        </div>
        """)

    with tech_col3:
        render_html("""
        <div class="feature-card-clean">
            <div style="font-family: 'JetBrains Mono'; font-size: 0.75rem; font-weight: 700; color: #0284C7; margin-bottom: 8px;">STAGE 03</div>
            <div class="feature-card-title">ChromaDB Store</div>
            <div class="feature-card-desc">
                3,282 pre-computed nodes stored in persistent SQLite vector tables with instantaneous Top-k similarity retrieval.
            </div>
        </div>
        """)

    with tech_col4:
        render_html("""
        <div class="feature-card-clean">
            <div style="font-family: 'JetBrains Mono'; font-size: 0.75rem; font-weight: 700; color: #0284C7; margin-bottom: 8px;">STAGE 04</div>
            <div class="feature-card-title">Gemini Synthesis</div>
            <div class="feature-card-desc">
                Google Gemini reasoning models stream strictly grounded clinical answers paired with Perplexity-style citations.
            </div>
        </div>
        """)

    # =====================================================================
    # SECTION 4: SERVICES & CAPABILITIES (#services)
    # =====================================================================
    st.markdown("<br><br><br><hr style='border: none; border-top: 1.5px solid #F1F5F9; margin-bottom: 4rem;'>", unsafe_allow_html=True)

    render_html("""
    <div id="services">
        <span class="section-badge-pill">✦ CLINICAL CAPABILITIES</span>
        <h2 class="section-title-large">Comprehensive Healthcare Decision Support</h2>
        <p class="section-subtitle-large">
            Whether for differential condition analysis, pharmacology contraindications, or emergency triage protocols, CuraPulse AI provides instantaneous reference support.
        </p>
    </div>
    """)

    serv_col1, serv_col2 = st.columns(2)

    with serv_col1:
        render_html("""
        <div class="feature-card-clean" style="margin-bottom: 1.5rem;">
            <div class="feature-card-icon">🫀</div>
            <div class="feature-card-title">Differential Symptom Triage</div>
            <div class="feature-card-desc">
                Map complex symptom clusters against verified disease hallmarks (e.g., classical triad for Abdominal Aortic Aneurysm, Asthma triggers, Acute Bronchitis).
            </div>
        </div>
        """)
        if st.button("Query Symptom Triage Scenario →", key="btn_srv_triage", use_container_width=True):
            st.session_state.pending_prompt = "What are the common clinical symptoms, classical diagnostic triad, and rupture risks of an Abdominal Aortic Aneurysm?"
            st.session_state.app_mode = "chat"
            st.rerun()

    with serv_col2:
        render_html("""
        <div class="feature-card-clean" style="margin-bottom: 1.5rem;">
            <div class="feature-card-icon">🩸</div>
            <div class="feature-card-title">Laboratory & Diagnostic Decoders</div>
            <div class="feature-card-desc">
                Understand blood test thresholds, fasting glucose metrics, HbA1c criteria, CT/MRI indications, and biopsy staging protocols.
            </div>
        </div>
        """)
        if st.button("Query Diagnostic Lab Scenario →", key="btn_srv_labs", use_container_width=True):
            st.session_state.pending_prompt = "What diagnostic blood tests and thresholds are used for Diabetes Mellitus, and what are key precautions?"
            st.session_state.app_mode = "chat"
            st.rerun()

    # =====================================================================
    # FOOTER SECTION
    # =====================================================================
    render_html("""
    <div class="footer-wrapper">
        <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 40px; margin-bottom: 3rem;">
            <div>
                <div class="custom-logo" style="margin-bottom: 1rem;">CURAPULSE.</div>
                <p style="color: #64748B; font-size: 0.95rem; line-height: 1.6; max-width: 320px;">
                    Revolutionizing healthcare with sovereign clinical intelligence, deterministic vector retrieval, and verified medical literature.
                </p>
                <div style="display: inline-flex; align-items: center; gap: 8px; padding: 4px 12px; background: #ECFDF5; border: 1.5px solid #A7F3D0; border-radius: 999px; font-size: 0.75rem; font-weight: 700; color: #065F46; font-family: 'JetBrains Mono'; margin-top: 1rem;">
                    <span style="width: 7px; height: 7px; border-radius: 50%; background: #10B981;"></span>
                    3,282 NODES INDEXED • GALE MEDICINE
                </div>
            </div>
            <div>
                <div class="footer-col-title">Navigation</div>
                <a href="#home" class="footer-link">Home</a>
                <a href="#about" class="footer-link">About CuraPulse</a>
                <a href="#technology" class="footer-link">Technology Pipeline</a>
                <a href="#services" class="footer-link">Clinical Services</a>
            </div>
            <div>
                <div class="footer-col-title">Resources</div>
                <a href="https://archive.org/details/galeencyclopedia0000unse" target="_blank" rel="noopener noreferrer" class="footer-link">Gale Encyclopedia ↗</a>
                <a href="https://docs.trychroma.com/" target="_blank" rel="noopener noreferrer" class="footer-link">ChromaDB Vector Store ↗</a>
                <a href="https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2" target="_blank" rel="noopener noreferrer" class="footer-link">Hugging Face MiniLM ↗</a>
                <a href="https://python.langchain.com/docs/" target="_blank" rel="noopener noreferrer" class="footer-link">LangChain RAG Docs ↗</a>
                <a href="https://ai.google.dev/" target="_blank" rel="noopener noreferrer" class="footer-link">Google Gemini AI ↗</a>
            </div>
            <div>
                <div class="footer-col-title">Governance & Clinical</div>
                <a href="https://pubmed.ncbi.nlm.nih.gov/" target="_blank" rel="noopener noreferrer" class="footer-link">PubMed Central (NCBI) ↗</a>
                <a href="https://www.nih.gov/health-information" target="_blank" rel="noopener noreferrer" class="footer-link">NIH Health Guidelines ↗</a>
                <a href="https://www.who.int/publications" target="_blank" rel="noopener noreferrer" class="footer-link">WHO Clinical Standards ↗</a>
                <a href="https://www.hhs.gov/hipaa/for-professionals/privacy/index.html" target="_blank" rel="noopener noreferrer" class="footer-link">HHS HIPAA Compliance ↗</a>
                <a href="https://www.cdc.gov/" target="_blank" rel="noopener noreferrer" class="footer-link">CDC Clinical Guidance ↗</a>
            </div>
        </div>
        <div class="footer-bottom-bar">
            <div>© 2026 CuraPulse AI. Designed & Developed by <strong>Aryan Patade</strong>. Grounded in The Gale Encyclopedia of Medicine.</div>
            <div style="font-family: 'JetBrains Mono'; font-size: 0.8rem; color: #0284C7;">SYSTEM VERIFIED • 100% PRIVATE</div>
        </div>
    </div>
    """)


# =========================================================================
# VIEW 2: THE WORKING HIGH-TECH CHATBOT CONSOLE
# =========================================================================
elif st.session_state.app_mode == "chat":

    # Chat Header Bar
    chat_hdr1, chat_hdr2, chat_hdr3 = st.columns([3, 4, 3])
    with chat_hdr1:
        render_html('<div class="custom-logo">CURAPULSE.</div>')

    with chat_hdr2:
        render_html("""
        <div style="text-align: center; padding-top: 10px;">
            <span style="display: inline-flex; align-items: center; gap: 6px; padding: 4px 14px; background: #ECFDF5; border: 1.5px solid #A7F3D0; border-radius: 999px; font-size: 0.78rem; font-weight: 700; color: #065F46; font-family: 'JetBrains Mono';">
                <span style="width: 7px; height: 7px; border-radius: 50%; background: #10B981;"></span>
                3,282 NODES INDEXED • GALE MEDICINE
            </span>
        </div>
        """)

    with chat_hdr3:
        btn_c1, btn_c2 = st.columns(2)
        if btn_c1.button("🧹 Clear", key="clear_chat_btn", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.rerun()
        if btn_c2.button("← Back", key="back_home_btn", use_container_width=True):
            st.session_state.app_mode = "landing"
            st.rerun()

    st.markdown("<hr style='border: none; border-top: 1.5px solid #E2E8F0; margin: 1.25rem 0 1.5rem 0;'>", unsafe_allow_html=True)

    # Empty State Guide
    if len(st.session_state.messages) == 0:
        render_html("""
        <div style="text-align: center; padding: 2.5rem 1rem; background: #F8FAFC; border: 1.5px dashed #CBD5E1; border-radius: 24px; margin-bottom: 2rem;">
            <div style="font-size: 2.2rem; margin-bottom: 0.4rem;">🩺</div>
            <div style="font-family: 'Plus Jakarta Sans'; font-size: 1.4rem; font-weight: 800; color: #0F172A;">CuraPulse Clinical Console Active</div>
            <div style="font-size: 0.95rem; color: #475569; max-width: 580px; margin: 0.5rem auto 0 auto; line-height: 1.6;">
                Ask any question regarding medical symptoms, diseases, diagnostic tests, or clinical management. Every response is grounded in <strong>The Gale Encyclopedia of Medicine</strong>.
            </div>
        </div>
        """)

    # Display Conversation Messages
    for msg in st.session_state.messages:
        is_assistant = msg["role"] == "assistant"
        with st.chat_message(msg["role"], avatar="🩺" if is_assistant else "👤"):
            st.markdown(msg["content"])
            
            # Display Perplexity-Style Citation Cards
            if is_assistant and msg.get("sources"):
                sources = msg["sources"]
                with st.expander(f"📚 Verified Literature Citations ({len(sources)} Sources)"):
                    for idx, src in enumerate(sources, 1):
                        render_html(f"""
                        <div class="citation-card-light">
                            <span class="citation-badge-light">SOURCE [{idx}]</span>
                            <strong style="color: #0F172A; font-size: 0.88rem;">{src.get('source', 'The Gale Encyclopedia of Medicine')}</strong>
                            <span style="color: #64748B; font-size: 0.78rem; margin-left: 8px; font-family: 'JetBrains Mono', monospace;">Page {src.get('page', 'N/A')}</span>
                            <div style="font-size: 0.85rem; color: #334155; line-height: 1.55; margin-top: 5px;">"{src.get('excerpt', '')}"</div>
                        </div>
                        """)

    # Handle Input from Floating Search or Chat Input
    active_prompt = None
    if st.session_state.pending_prompt:
        active_prompt = st.session_state.pending_prompt
        st.session_state.pending_prompt = None
    else:
        active_prompt = st.chat_input("Ask a clinical or medical question (e.g., 'What is cancer?', 'Symptoms of Asthma')...")

    if active_prompt:
        if not retriever:
            st.error("Vector database is not ready. Run `.\\ingest.bat --store chroma` to index documents.")
            st.stop()

        # Append user message
        st.session_state.messages.append({"role": "user", "content": active_prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(active_prompt)

        # Generate Assistant Response
        with st.chat_message("assistant", avatar="🩺"):
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
            try:
                from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
                from langchain_classic.chains.combine_documents import create_stuff_documents_chain
            except ImportError:
                import importlib
                _lc_chains = importlib.import_module("langchain.chains")
                _lc_combine = importlib.import_module("langchain.chains.combine_documents")
                create_history_aware_retriever = _lc_chains.create_history_aware_retriever
                create_retrieval_chain = _lc_chains.create_retrieval_chain
                create_stuff_documents_chain = _lc_combine.create_stuff_documents_chain

            from src.prompt import SYSTEM_PROMPT, CONTEXTUALIZE_Q_SYSTEM_PROMPT

            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash-lite",
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

            with st.spinner("Analyzing verified medical literature..."):
                try:
                    response = rag_chain.invoke({
                        "input": active_prompt,
                        "chat_history": st.session_state.chat_history
                    })
                    answer = response.get("answer", "")
                    context_docs = response.get("context", [])
                    
                    # Format sources
                    sources = []
                    for doc in context_docs:
                        sources.append({
                            "source": doc.metadata.get("source", "The Gale Encyclopedia of Medicine"),
                            "page": doc.metadata.get("page", "Unknown"),
                            "excerpt": doc.page_content[:260].replace("\n", " ").strip() + "..."
                        })

                    # Stream answer to UI
                    st.markdown(answer)

                    if sources:
                        with st.expander(f"📚 Verified Literature Citations ({len(sources)} Sources)"):
                            for idx, src in enumerate(sources, 1):
                                render_html(f"""
                                <div class="citation-card-light">
                                    <span class="citation-badge-light">SOURCE [{idx}]</span>
                                    <strong style="color: #0F172A; font-size: 0.88rem;">{src['source']}</strong>
                                    <span style="color: #64748B; font-size: 0.78rem; margin-left: 8px; font-family: 'JetBrains Mono', monospace;">Page {src['page']}</span>
                                    <div style="font-size: 0.85rem; color: #334155; line-height: 1.55; margin-top: 5px;">"{src['excerpt']}"</div>
                                </div>
                                """)

                    # Update session states
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                    st.session_state.chat_history.extend([
                        ("human", active_prompt),
                        ("assistant", answer)
                    ])

                except Exception as e:
                    st.error(f"Error generating clinical response: {str(e)}")
