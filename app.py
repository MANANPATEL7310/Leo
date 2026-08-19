import streamlit as st
import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Leo | AI Executive Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS implementing the complete DataWars-style dark indigo design system
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg-base: #12152C;
        --bg-gradient-start: #161A38;
        --bg-gradient-end: #272C55;
        --bg-nav: #0A0B14;
        --accent-primary: #5B5FEF;
        --accent-primary-hover: #4A4FE0;
        --accent-soft: #A5B4FC;
        --text-primary: #F5F6FF;
        --text-secondary: #B8BCD9;
        --text-muted: #6E7299;
        --border-subtle: rgba(255, 255, 255, 0.08);
        --border-card: rgba(165, 180, 252, 0.15);
        --shape-fill: rgba(165, 180, 252, 0.05);
    }

    /* Overall Page Background & Typography */
    .stApp {
        background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-base) 50%, var(--bg-gradient-end) 100%) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--text-primary) !important;
        min-height: 100vh;
    }

    /* Ambient Background Decorative Shapes */
    .bg-shape-1 {
        position: fixed;
        top: -120px;
        right: -80px;
        width: 480px;
        height: 480px;
        background: var(--shape-fill);
        border-radius: 50%;
        filter: blur(80px);
        pointer-events: none;
        z-index: 0;
    }

    .bg-shape-2 {
        position: fixed;
        bottom: 10%;
        left: -100px;
        width: 520px;
        height: 520px;
        background: rgba(91, 95, 239, 0.04);
        border-radius: 50%;
        filter: blur(100px);
        pointer-events: none;
        z-index: 0;
    }

    /* Hide Default Streamlit Header Decoration */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Sidebar Custom Styling */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-nav) !important;
        border-right: 1px solid var(--border-subtle) !important;
        padding-top: 1rem;
    }

    section[data-testid="stSidebar"] hr {
        border-color: var(--border-subtle) !important;
        margin: 1.25rem 0 !important;
    }

    .sidebar-section-label {
        font-size: 11px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: var(--text-muted) !important;
        margin-bottom: 0.75rem !important;
    }

    .sidebar-brand-title {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: var(--text-primary);
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .sidebar-brand-sub {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin-top: 2px;
        margin-bottom: 12px;
    }

    /* Status Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        padding: 4px 10px;
        border-radius: 6px;
        margin-bottom: 8px;
    }

    .status-connected {
        background: rgba(52, 211, 153, 0.1);
        border: 1px solid rgba(52, 211, 153, 0.25);
        color: #34D399;
    }

    .status-disconnected {
        background: rgba(248, 113, 113, 0.1);
        border: 1px solid rgba(248, 113, 113, 0.25);
        color: #F87171;
    }

    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        display: inline-block;
    }

    .dot-active {
        background-color: #34D399;
        box-shadow: 0 0 6px rgba(52, 211, 153, 0.6);
    }

    .dot-inactive {
        background-color: #6E7299;
    }

    /* Integration Tool Row Item */
    .tool-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 10px;
        border-radius: 8px;
        margin-bottom: 4px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid transparent;
        transition: all 0.15s ease;
    }

    .tool-row:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: var(--border-subtle);
    }

    .tool-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .tool-name {
        font-size: 0.85rem;
        font-weight: 500;
        color: var(--text-primary);
    }

    .tool-desc {
        font-size: 0.75rem;
        color: var(--text-muted);
    }

    /* Quick Prompt Buttons (Tappable Suggestion Cards) */
    div[data-testid="stSidebar"] .stButton > button {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 10px !important;
        color: var(--text-secondary) !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        text-align: left !important;
        padding: 10px 12px !important;
        margin-bottom: 6px !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
    }

    div[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(91, 95, 239, 0.08) !important;
        border-color: var(--border-card) !important;
        color: var(--text-primary) !important;
        transform: translateY(-1px);
    }

    /* Centered Hero Section */
    .hero-wrapper {
        position: relative;
        z-index: 1;
        padding: 1.5rem 0 2rem 0;
        max-width: 820px;
        margin: 0 auto;
        text-align: center;
    }

    .hero-heading {
        font-size: 2.75rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.15;
        color: var(--text-primary);
        margin-bottom: 0.85rem;
    }

    .hero-subtext {
        font-size: 1.05rem;
        font-weight: 400;
        color: var(--text-secondary);
        line-height: 1.6;
        max-width: 640px;
        margin: 0 auto 1.75rem auto;
    }

    /* Stat Row Pattern - Centered */
    .stat-row {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        gap: 3rem;
        padding: 1.25rem 0;
        border-top: 1px solid var(--border-subtle);
        border-bottom: 1px solid var(--border-subtle);
        margin: 0 auto 1.5rem auto;
    }

    .stat-item {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .stat-number {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: var(--accent-soft);
        line-height: 1.1;
    }

    .stat-label {
        font-size: 0.75rem;
        font-weight: 500;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 4px;
    }

    /* Secondary Feature List with Vertical Dividers - Centered */
    .secondary-feature-row {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        gap: 12px;
        font-size: 0.82rem;
        color: var(--text-secondary);
    }

    .feature-divider {
        color: var(--border-subtle);
        font-weight: 300;
    }

    /* Chat Messages */
    .stChatMessage {
        background: rgba(18, 21, 44, 0.6) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        margin-bottom: 14px !important;
        backdrop-filter: blur(8px);
    }

    /* Chat Input Styling */
    div[data-testid="stChatInput"] {
        border-radius: 14px !important;
        background-color: var(--bg-nav) !important;
        border: 1px solid var(--border-subtle) !important;
        box-shadow: none !important;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: var(--accent-primary) !important;
    }

    div[data-testid="stChatInput"] textarea {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary) !important;
    }

    div[data-testid="stChatInput"] button {
        background-color: var(--accent-primary) !important;
        color: #ffffff !important;
        border-radius: 50% !important;
        border: none !important;
        transition: background-color 0.2s ease !important;
    }

    div[data-testid="stChatInput"] button:hover {
        background-color: var(--accent-primary-hover) !important;
    }
</style>
""", unsafe_allow_html=True)

# Render decorative ambient background shapes
st.markdown('<div class="bg-shape-1"></div><div class="bg-shape-2"></div>', unsafe_allow_html=True)

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None

# Webhook configuration
webhook_url = os.getenv("N8N_WEBHOOK_URL", "").strip()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="sidebar-brand-title">Leo Executive</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-brand-sub">Autonomous Agentic Workflow</div>', unsafe_allow_html=True)
    
    # Status Badge
    if webhook_url:
        st.markdown(
            '<div class="status-badge status-connected"><span class="status-dot dot-active"></span> Webhook Connected</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="status-badge status-disconnected"><span class="status-dot dot-inactive"></span> Missing Webhook URL</div>',
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # SECTION 1: Connected Workspace Tools
    st.markdown('<div class="sidebar-section-label">Connected Workspace Tools</div>', unsafe_allow_html=True)
    
    tools = [
        ("Google Calendar", "Schedules & Events", True),
        ("Gmail Inbox", "Read, Summarize, Send", True),
        ("Google Tasks", "To-Dos & Reminders", True),
        ("Google Docs", "Executive Notes", True),
        ("Google Sheets", "Expense Ledger", True),
        ("Web Search", "Real-Time Research", True),
    ]
    
    for name, desc, connected in tools:
        dot_class = "dot-active" if (connected and webhook_url) else "dot-inactive"
        st.markdown(f"""
        <div class="tool-row">
            <div class="tool-left">
                <span class="status-dot {dot_class}"></span>
                <span class="tool-name">{name}</span>
            </div>
            <span class="tool-desc">{desc}</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    # SECTION 2: Prompt Suggestions / Quick Actions
    st.markdown('<div class="sidebar-section-label">Quick Suggestions</div>', unsafe_allow_html=True)
    
    quick_actions = [
        "What's on my schedule for today?",
        "Summarize my unread emails from this morning",
        "Add task: Review Q3 strategy deck",
        "Record expense: $42 for client lunch",
        "Append note: Key decisions from leadership sync",
    ]
    
    for prompt in quick_actions:
        if st.button(prompt, key=f"quick_{prompt}", use_container_width=True):
            st.session_state.quick_prompt = prompt
            st.rerun()

    st.markdown("---")
    
    # SECTION 3: Session Controls
    st.markdown('<div class="sidebar-section-label">Session Controls</div>', unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.quick_prompt = None
            st.rerun()
    with col_c2:
        if st.session_state.messages:
            chat_export = json.dumps(st.session_state.messages, indent=2)
            st.download_button(
                label="Export",
                data=chat_export,
                file_name=f"leo_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )


# --- MAIN HERO / HEADER SECTION ---

st.markdown("""
<div class="hero-wrapper">
    <div class="hero-heading">
        Executive clarity.<br/>Automated workflow.
    </div>
    <div class="hero-subtext">
        Leo manages your calendar, orchestrates email communications, tracks critical tasks, logs expenses, and conducts live research through a unified n8n agentic workflow.
    </div>
    <div class="stat-row">
        <div class="stat-item">
            <span class="stat-number">6</span>
            <span class="stat-label">Connected Tools</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">&lt; 2s</span>
            <span class="stat-label">Avg Execution</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">100%</span>
            <span class="stat-label">Privacy First</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">99.9%</span>
            <span class="stat-label">Workflow Uptime</span>
        </div>
    </div>
    <div class="secondary-feature-row">
        <span>Calendar Scheduling</span>
        <span class="feature-divider">|</span>
        <span>Inbox Synthesis</span>
        <span class="feature-divider">|</span>
        <span>Google Tasks</span>
        <span class="feature-divider">|</span>
        <span>Executive Docs</span>
        <span class="feature-divider">|</span>
        <span>Expense Tracking</span>
        <span class="feature-divider">|</span>
        <span>Live Search</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Missing Webhook Warning
if not webhook_url:
    st.warning("`N8N_WEBHOOK_URL` is not set in `.env`. Configure your webhook URL to enable live executions.", icon="⚠️")

# Display Message History
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "⚡"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Handle quick prompt selection from sidebar
pending_prompt = None
if st.session_state.quick_prompt:
    pending_prompt = st.session_state.quick_prompt
    st.session_state.quick_prompt = None

# Chat Input Bar with refined placeholder
user_message = st.chat_input("Message Leo... (e.g. Schedule a meeting tomorrow at 10 AM, summarize unread emails)")

# Determine final message to send
active_message = user_message or pending_prompt

if active_message:
    # Append & render User Message
    st.session_state.messages.append({"role": "user", "content": active_message})
    with st.chat_message("user", avatar="👤"):
        st.markdown(active_message)

    # Process response via n8n webhook
    with st.chat_message("assistant", avatar="⚡"):
        if not webhook_url:
            error_msg = "Error: No n8n webhook URL configured. Please set `N8N_WEBHOOK_URL` in your `.env` file."
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
        else:
            with st.spinner("Executing workflow..."):
                try:
                    response = requests.post(
                        webhook_url,
                        json={"message": active_message},
                        timeout=120
                    )
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            if isinstance(data, list) and len(data) > 0 and "output" in data[0]:
                                ai_response = data[0]["output"]
                            elif isinstance(data, dict) and "output" in data:
                                ai_response = data["output"]
                            elif isinstance(data, dict) and "text" in data:
                                ai_response = data["text"]
                            else:
                                ai_response = str(data)
                        except Exception:
                            ai_response = response.text
                        
                        st.markdown(ai_response)
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    else:
                        error_msg = f"Webhook returned status `{response.status_code}`: {response.text}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

                except requests.exceptions.Timeout:
                    error_msg = "Request timed out after 120 seconds. Please check your n8n workflow execution."
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                except requests.exceptions.ConnectionError:
                    error_msg = "Connection error: Unable to reach n8n webhook URL. Ensure your n8n instance is active."
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                except Exception as e:
                    error_msg = f"Unexpected error: `{str(e)}`"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})