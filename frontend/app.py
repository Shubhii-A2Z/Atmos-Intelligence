from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import streamlit as st

from src.client import build_client, select_provider
from src import run_agent_turn
from src.prompts.prompts import (
    build_greeting_prompt,
    build_system_prompt,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AtmosAI",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(59, 130, 246, 0.12),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 0%,
                rgba(139, 92, 246, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(14, 165, 233, 0.06),
                transparent 35%
            ),
            #070a11;

        color: #f8fafc;
    }

    .main .block-container {
        max-width: 1080px;

        padding-top: 2.2rem;
        padding-bottom: 8rem;
    }


    /* ========================================================
       REMOVE DEFAULT STREAMLIT TOP SPACE
       ======================================================== */

    header[data-testid="stHeader"] {
        background: transparent;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0b0f18 0%,
                #080b12 100%
            );

        border-right:
            1px solid rgba(255, 255, 255, 0.065);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.4rem;
    }

    section[data-testid="stSidebar"] hr {
        border-color:
            rgba(255, 255, 255, 0.07);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f8fafc;
    }

    section[data-testid="stSidebar"] p {
        color: #94a3b8;
    }


    /* ========================================================
       SIDEBAR BUTTON
       ======================================================== */

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;

        border-radius: 13px;

        border:
            1px solid rgba(255, 255, 255, 0.07);

        background:
            rgba(255, 255, 255, 0.035);

        color: #cbd5e1;

        transition:
            transform 0.18s ease,
            background 0.18s ease,
            border-color 0.18s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-1px);

        background:
            rgba(59, 130, 246, 0.09);

        border-color:
            rgba(96, 165, 250, 0.28);

        color: white;
    }


    /* ========================================================
       MAIN TITLE
       ======================================================== */

    .main h1 {
        font-size: clamp(42px, 6vw, 64px);

        line-height: 0.98;

        letter-spacing: -3px;

        font-weight: 850;

        color: #ffffff;

        margin-bottom: 0.55rem;
    }


    /* ========================================================
       HERO DESCRIPTION
       ======================================================== */

    .hero-description {
        font-size: 16px;

        line-height: 1.7;

        color: #94a3b8;

        max-width: 650px;

        margin-bottom: 1.2rem;
    }


    /* ========================================================
       STATUS
       ======================================================== */

    .status-pill {
        display: inline-block;

        padding: 6px 12px;

        border-radius: 999px;

        background:
            rgba(34, 197, 94, 0.07);

        border:
            1px solid rgba(34, 197, 94, 0.15);

        color: #86efac;

        font-size: 11px;

        font-weight: 600;

        letter-spacing: 0.02em;
    }


    /* ========================================================
       SUGGESTION CARDS
       ======================================================== */

    div[data-testid="stHorizontalBlock"] {
        gap: 0.8rem;
    }

    .suggestion-title {
        color: #64748b;

        font-size: 11px;

        text-transform: uppercase;

        letter-spacing: 0.12em;

        font-weight: 700;

        margin-top: 1.8rem;

        margin-bottom: 0.7rem;
    }

    .suggestion-card {
        min-height: 105px;

        padding: 17px;

        border-radius: 17px;

        background:
            linear-gradient(
                145deg,
                rgba(255, 255, 255, 0.045),
                rgba(255, 255, 255, 0.018)
            );

        border:
            1px solid rgba(255, 255, 255, 0.07);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            background 0.2s ease;

        cursor: default;
    }

    .suggestion-card:hover {
        transform: translateY(-3px);

        background:
            rgba(59, 130, 246, 0.06);

        border-color:
            rgba(96, 165, 250, 0.20);
    }

    .suggestion-icon {
        font-size: 20px;

        margin-bottom: 9px;
    }

    .suggestion-text {
        color: #cbd5e1;

        font-size: 12px;

        line-height: 1.45;
    }


    /* ========================================================
       CHAT
       ======================================================== */

    [data-testid="stChatMessage"] {
        background: transparent;

        border: none;

        padding-top: 0.7rem;
        padding-bottom: 0.7rem;
    }

    [data-testid="stChatMessageContent"] {
        font-size: 14px;

        line-height: 1.75;
    }


    /* ========================================================
       USER MESSAGE
       ======================================================== */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    )
    [data-testid="stChatMessageContent"] {

        background:
            linear-gradient(
                135deg,
                rgba(37, 99, 235, 0.17),
                rgba(59, 130, 246, 0.08)
            );

        border:
            1px solid rgba(96, 165, 250, 0.12);

        border-radius:
            19px 19px 5px 19px;

        padding:
            13px 17px;
    }


    /* ========================================================
       ASSISTANT MESSAGE
       ======================================================== */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    )
    [data-testid="stChatMessageContent"] {

        background:
            linear-gradient(
                145deg,
                rgba(255, 255, 255, 0.045),
                rgba(255, 255, 255, 0.018)
            );

        border:
            1px solid rgba(255, 255, 255, 0.065);

        border-radius:
            5px 19px 19px 19px;

        padding:
            15px 19px;

        box-shadow:
            0 10px 35px rgba(0, 0, 0, 0.16);
    }


    /* ========================================================
       CHAT INPUT
       ======================================================== */

    [data-testid="stChatInput"] {
        padding-bottom: 1.5rem;
    }

    [data-testid="stChatInput"] > div {

        border-radius: 20px !important;

        background:
            rgba(10, 15, 26, 0.94) !important;

        border:
            1px solid rgba(148, 163, 184, 0.15) !important;

        box-shadow:
            0 0 0 1px rgba(255, 255, 255, 0.015),
            0 18px 60px rgba(0, 0, 0, 0.42) !important;

        transition:
            border-color 0.2s ease,
            box-shadow 0.2s ease !important;
    }

    [data-testid="stChatInput"] > div:focus-within {

        border-color:
            rgba(96, 165, 250, 0.45) !important;

        box-shadow:
            0 0 0 4px rgba(59, 130, 246, 0.07),
            0 18px 65px rgba(0, 0, 0, 0.48) !important;
    }

    [data-testid="stChatInput"] textarea {

        color: #f8fafc !important;

        font-size: 14px !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {

        color: #64748b !important;
    }


    /* ========================================================
       EXPANDER
       ======================================================== */

    [data-testid="stExpander"] {

        border-radius: 14px;

        background:
            rgba(255, 255, 255, 0.025);

        border:
            1px solid rgba(255, 255, 255, 0.07);
    }


    /* ========================================================
       INFO / SUCCESS
       ======================================================== */

    [data-testid="stAlert"] {

        border-radius: 14px;

        border:
            1px solid rgba(96, 165, 250, 0.12);
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .main .block-container {

            padding-left: 1rem;
            padding-right: 1rem;

            padding-top: 1.5rem;
        }

        .main h1 {

            font-size: 40px;

            letter-spacing: -2px;
        }

        .hero-description {

            font-size: 14px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # Brand
    # --------------------------------------------------------

    st.title("🌤️ AtmosAI")

    st.caption(
        "Your intelligent weather companion"
    )

    st.divider()


    # --------------------------------------------------------
    # About
    # --------------------------------------------------------

    st.subheader("About")

    st.write(
        build_greeting_prompt()
    )


    st.divider()


    # --------------------------------------------------------
    # Provider
    # --------------------------------------------------------

    st.subheader("AI Provider")

    provider = None
    _client = None
    model = None

    try:

        provider = select_provider()

        _client = build_client(provider)

        model = provider.model

        st.success(
            f"✦ {provider.name}"
        )

        st.caption(
            f"Model · {model}"
        )

    except RuntimeError:

        st.error(
            "Unable to initialize the AI provider."
        )


    st.divider()


    # --------------------------------------------------------
    # Agent Configuration
    # --------------------------------------------------------

    st.subheader("Agent")

    st.caption(
        "System instructions used by AtmosAI."
    )

    with st.expander(
        "View system prompt",
        expanded=False,
    ):

        st.code(
            build_system_prompt(),
            language="markdown",
        )


    st.divider()


    # --------------------------------------------------------
    # Clear conversation
    # --------------------------------------------------------

    if st.button(
        "🗑️  Clear conversation",
        use_container_width=True,
    ):

        st.session_state.chat_log = []

        st.rerun()


# ============================================================
# MAIN HERO
# ============================================================

if not st.session_state.chat_log:

    # --------------------------------------------------------
    # Empty-state hero
    # --------------------------------------------------------

    st.caption(
        "✦  AI WEATHER ASSISTANT"
    )

    st.title(
        "Weather, understood."
    )

    st.markdown(
        """
        <div class="hero-description">
        Ask AtmosAI about forecasts, conditions,
        temperatures, rain, locations, and more.
        Get useful answers through natural conversation.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="status-pill">●  AtmosAI is ready</div>',
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # Suggestions
    # --------------------------------------------------------

    st.markdown(
        '<div class="suggestion-title">Try asking</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="suggestion-card">
                <div class="suggestion-icon">☀️</div>
                <div class="suggestion-text">
                    What's the weather like in Delhi today?
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            """
            <div class="suggestion-card">
                <div class="suggestion-icon">🌧️</div>
                <div class="suggestion-text">
                    Will it rain tomorrow?
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            """
            <div class="suggestion-card">
                <div class="suggestion-icon">🌡️</div>
                <div class="suggestion-text">
                    What's the temperature right now?
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    st.markdown("")


# ============================================================
# CHAT HISTORY
# ============================================================

for entry in st.session_state.chat_log:

    if entry.get("content"):

        with st.chat_message(
            entry["role"]
        ):

            st.markdown(
                entry["content"]
            )


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input(
    "Ask AtmosAI anything about the weather..."
)


# ============================================================
# AGENT TURN
# ============================================================

if prompt:

    # --------------------------------------------------------
    # USER
    # --------------------------------------------------------

    st.session_state.chat_log.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)


    # --------------------------------------------------------
    # ASSISTANT
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "AtmosAI is thinking..."
        ):

            try:

                answer = run_agent_turn(
                    st.session_state.chat_log
                )

            except Exception as e:

                st.error(
                    "Something went wrong while "
                    "processing your request."
                )

                answer = str(e)

        st.markdown(answer)


    # --------------------------------------------------------
    # SAVE ASSISTANT MESSAGE
    # --------------------------------------------------------

    st.session_state.chat_log.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )