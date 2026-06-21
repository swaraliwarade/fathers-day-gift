"""
Happy Father's Day, Dad ❤️
A personalized, animated, interactive Streamlit web app
built as a heartfelt digital gift for Dad.

Run with:
    streamlit run app.py
"""

import streamlit as st
import random
import time
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Happy Father's Day, Dad ❤️",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
def init_session_state():
    """Initialize all session state variables used across the app."""
    defaults = {
        "quiz_started": False,
        "quiz_index": 0,
        "quiz_score": 0,
        "quiz_answers": [],
        "quiz_done": False,
        "surprise_clicked": False,
        "thank_you_notes": [
            {"name": "Mom", "note": "You are my partner in everything. I love you!"},
            {"name": "swarali", "note": "Thank you for being my hero, always. I love you!"},
        ],
        "flipped_cards": set(),
        "uploaded_photos": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()

# ============================================================
# CUSTOM CSS — THEME, ANIMATIONS, GLASSMORPHISM, RESPONSIVENESS
# ============================================================
def load_css():
    """Inject all custom CSS for theme, animations, and layout."""
    st.markdown(
        """
        <style>
        /* ---------- COLOR PALETTE ----------
           Navy Blue:  #1B2A4A
           Soft Gold:  #D4AF37
           Cream:      #FFF8E7
           Sky Blue:   #A7D8F0
        ------------------------------------ */

        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Dancing+Script:wght@600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        /* ---------- ANIMATED GRADIENT BACKGROUND ---------- */
        .stApp {
            background: linear-gradient(-45deg, #1B2A4A, #2c4270, #A7D8F0, #FFF8E7);
            background-size: 400% 400%;
            animation: gradientShift 18s ease infinite;
        }

        @keyframes gradientShift {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        /* ---------- FLOATING HEARTS / STARS LAYER ---------- */
        .floaters {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            overflow: hidden;
            pointer-events: none;
            z-index: 0;
        }

        .floater {
            position: absolute;
            bottom: -10%;
            font-size: 24px;
            opacity: 0.55;
            animation-name: floatUp;
            animation-timing-function: linear;
            animation-iteration-count: infinite;
        }

        @keyframes floatUp {
            0%   { transform: translateY(0) rotate(0deg); opacity: 0; }
            10%  { opacity: 0.6; }
            90%  { opacity: 0.6; }
            100% { transform: translateY(-110vh) rotate(360deg); opacity: 0; }
        }

        /* ---------- HERO TITLE ---------- */
        .hero-title {
            text-align: center;
            font-size: 3.4rem;
            font-weight: 800;
            color: #FFF8E7;
            text-shadow: 0 4px 18px rgba(0,0,0,0.35);
            margin-bottom: 0.2rem;
            animation: popIn 1.2s ease-out;
        }

        @keyframes popIn {
            0% { transform: scale(0.7); opacity: 0; }
            70% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(1); }
        }

        .hero-subtitle {
            text-align: center;
            font-family: 'Dancing Script', cursive;
            font-size: 1.8rem;
            color: #D4AF37;
            animation: fadeInUp 1.8s ease-out;
            margin-bottom: 1.5rem;
        }

        @keyframes fadeInUp {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        .banner {
            text-align: center;
            font-size: 1.1rem;
            background: linear-gradient(90deg, #D4AF37, #FFF8E7, #D4AF37);
            background-size: 200% auto;
            animation: shine 3.5s linear infinite;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 600;
            margin-bottom: 1rem;
        }

        @keyframes shine {
            to { background-position: 200% center; }
        }

        /* ---------- GLASSMORPHISM CARD ---------- */
        .glass-card {
            background: rgba(255, 248, 231, 0.15);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
            padding: 2rem 2.5rem;
            color: #FFF8E7;
            font-size: 1.15rem;
            line-height: 1.9;
            margin: 1rem 0 2rem 0;
            animation: fadeInUp 1.5s ease-out;
        }

        .glass-card .signature {
            font-family: 'Dancing Script', cursive;
            font-size: 1.6rem;
            color: #D4AF37;
            display: block;
            margin-top: 1rem;
        }

        /* ---------- SECTION HEADERS ---------- */
        .section-header {
            color: #FFF8E7;
            font-size: 2rem;
            font-weight: 700;
            text-align: center;
            margin-top: 2.5rem;
            margin-bottom: 1.2rem;
            text-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }
        .section-header span { color: #D4AF37; }

        /* ---------- REASON FLIP CARDS ---------- */
        .reason-card {
            background: rgba(167, 216, 240, 0.18);
            border: 1px solid rgba(212, 175, 55, 0.4);
            border-radius: 16px;
            padding: 1.4rem;
            text-align: center;
            color: #FFF8E7;
            font-weight: 500;
            min-height: 110px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.35s ease, background 0.35s ease;
            box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        }
        .reason-card:hover {
            transform: translateY(-8px) scale(1.03);
            background: rgba(212, 175, 55, 0.28);
        }

        /* ---------- GALLERY ---------- */
        .gallery-caption {
            text-align: center;
            color: #FFF8E7;
            font-size: 0.9rem;
            margin-top: 0.3rem;
        }

        /* ---------- STICKY NOTES ---------- */
        .sticky-note {
            background: #FFF3B0;
            color: #1B2A4A;
            padding: 1rem;
            border-radius: 4px 4px 16px 4px;
            box-shadow: 4px 6px 14px rgba(0,0,0,0.3);
            font-weight: 500;
            min-height: 110px;
            transform: rotate(-2deg);
            transition: transform 0.25s ease;
            font-size: 0.95rem;
        }
        .sticky-note:nth-child(2n) { transform: rotate(2deg); background: #C9E9FF; }
        .sticky-note:nth-child(3n) { transform: rotate(-1.5deg); background: #FFD9D9; }
        .sticky-note:hover { transform: rotate(0deg) scale(1.04); }
        .sticky-name {
            font-family: 'Dancing Script', cursive;
            font-size: 1.2rem;
            margin-top: 0.5rem;
            display: block;
        }

        /* ---------- FOOTER ---------- */
        .footer {
            text-align: center;
            color: #FFF8E7;
            opacity: 0.85;
            font-size: 0.95rem;
            margin-top: 3rem;
            padding: 1.5rem 0;
            border-top: 1px solid rgba(255,255,255,0.2);
        }

        /* ---------- BUTTON STYLING ---------- */
        div.stButton > button {
            background: linear-gradient(135deg, #D4AF37, #f0d878);
            color: #1B2A4A;
            font-weight: 700;
            border: none;
            border-radius: 14px;
            padding: 0.6rem 1.4rem;
            box-shadow: 0 4px 14px rgba(0,0,0,0.25);
            transition: transform 0.2s ease;
        }
        div.stButton > button:hover {
            transform: translateY(-3px) scale(1.03);
            color: #1B2A4A;
        }

        /* ---------- SURPRISE BUTTON ---------- */
        .surprise-msg {
            text-align: center;
            font-size: 2rem;
            font-weight: 800;
            color: #D4AF37;
            animation: popIn 1s ease-out, glow 2s ease-in-out infinite alternate;
            margin-top: 1rem;
        }
        @keyframes glow {
            from { text-shadow: 0 0 10px rgba(212,175,55,0.6); }
            to   { text-shadow: 0 0 25px rgba(212,175,55,1); }
        }

        /* Responsive tweaks */
        @media (max-width: 768px) {
            .hero-title { font-size: 2.2rem; }
            .hero-subtitle { font-size: 1.3rem; }
            .glass-card { padding: 1.2rem 1.4rem; font-size: 1rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_floating_background():
    """Render floating hearts/stars decorative layer using pure CSS/HTML."""
    symbols = ["❤️", "⭐", "💛", "✨", "💙"]
    floaters_html = '<div class="floaters">'
    for i in range(18):
        symbol = random.choice(symbols)
        left = random.randint(0, 100)
        duration = random.randint(10, 22)
        delay = random.randint(0, 15)
        size = random.randint(16, 30)
        floaters_html += (
            f'<span class="floater" style="left:{left}%; '
            f"font-size:{size}px; animation-duration:{duration}s; "
            f'animation-delay:{delay}s;">{symbol}</span>'
        )
    floaters_html += "</div>"
    st.markdown(floaters_html, unsafe_allow_html=True)


# ============================================================
# SECTION: WELCOME / HERO
# ============================================================
def render_hero():
    """Render the welcome screen and hero section with title and banner."""
    st.markdown('<div class="hero-title">Happy Father\'s Day, Dad ❤️</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">A small gift made with love.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="banner">🎉 Celebrating the World\'s Greatest Dad 🎉</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
            <div style="text-align:center; font-size:6rem; line-height:1.1;
                        animation: fadeInUp 1.6s ease-out;">
                👨‍👧‍👦
            </div>
            <div style="text-align:center; color:#FFF8E7; font-style:italic;
                        opacity:0.9; margin-top:-0.5rem;">
                Forever my hero, my DAD.
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# SECTION: PERSONAL MESSAGE
# ============================================================
def render_personal_message():
    """Render the heartfelt personal message inside a glassmorphism card."""
    st.markdown('<div class="section-header">💌 A Letter For <span>You</span></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="glass-card">
            Dear Dad,<br><br>
            Thank you for always supporting me, encouraging me, and believing in me.
            Your guidance, patience, and love means more than words can express.<br><br>
            I am grateful for everything you've taught me and every sacrifice you've made.<br><br>
            Happy Father's Day! I love you.
            <span class="signature">❤️ swarali </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SECTION: MEMORY GALLERY
# ============================================================
def render_gallery():
    """Render an uploadable, grid-style photo gallery with hover effects."""
    st.markdown('<div class="section-header">📸 Memory <span>Gallery</span></div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; color:#FFF8E7; opacity:0.85;'>"
        "Upload your favorite memories together below.</p>",
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader(
        "Upload family photos",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded:
        st.session_state.uploaded_photos = uploaded

    photos = st.session_state.uploaded_photos

    if photos:
        cols = st.columns(3)
        for idx, photo in enumerate(photos):
            with cols[idx % 3]:
                st.image(photo, use_container_width=True, caption=None)
                st.markdown(
                    f"<div class='gallery-caption'>Memory #{idx + 1} 💕</div>",
                    unsafe_allow_html=True,
                )
    else:
        st.markdown(
            "<p style='text-align:center; color:#FFF8E7; opacity:0.6;'>"
            "No photos yet — add some treasured moments above! 🖼️</p>",
            unsafe_allow_html=True,
        )


# ============================================================
# SECTION: REASONS WHY YOU'RE THE BEST DAD (FLIP-STYLE CARDS)
# ============================================================
REASONS = [
    ("🤝", "You always help me with decisions", "In every choice I make, you're right there helping me choose the best path."),
    ("😂", "You are very funny", "Even your unfunny jokes make me laugh hard."),
    ("📚", "You teach me lessons", "The wisdom you've shared will guide me forever."),
    ("💪", "You work hard for our family", "Every sacrifice you've made hasn't gone unnoticed."),
    ("🌟", "You inspire me", "Watching you has taught me how to be a better person."),
]


def render_reasons():
    """Render interactive cards that reveal a deeper note when clicked."""
    st.markdown('<div class="section-header">🏆 Reasons You\'re The <span>Best Dad</span></div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; color:#FFF8E7; opacity:0.85;'>Click a card to reveal why ✨</p>",
        unsafe_allow_html=True,
    )

    cols = st.columns(len(REASONS))
    for idx, (emoji, title, detail) in enumerate(REASONS):
        with cols[idx]:
            is_flipped = idx in st.session_state.flipped_cards
            label = f"{emoji}\n\n{detail}" if is_flipped else f"{emoji}\n\n{title}"
            if st.button(label, key=f"reason_{idx}", use_container_width=True):
                if is_flipped:
                    st.session_state.flipped_cards.discard(idx)
                else:
                    st.session_state.flipped_cards.add(idx)
                st.rerun()


# ============================================================
# SECTION: THANK YOU WALL (STICKY NOTES)
# ============================================================
def render_thank_you_wall():
    """Render a digital sticky-note board where family can add appreciation notes."""
    st.markdown('<div class="section-header">📌 Thank You <span>Wall</span></div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; color:#FFF8E7; opacity:0.85;'>"
        "Leave a sweet note for Dad below 💛</p>",
        unsafe_allow_html=True,
    )

    with st.form("note_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 3])
        with col1:
            name = st.text_input("Your name", placeholder="Your name")
        with col2:
            note = st.text_input("Your note", placeholder="Write something sweet...")
        submitted = st.form_submit_button("📌 Pin Note")
        if submitted and note.strip():
            st.session_state.thank_you_notes.append(
                {"name": name.strip() if name.strip() else "Anonymous", "note": note.strip()}
            )
            st.rerun()

    notes = st.session_state.thank_you_notes
    if notes:
        cols = st.columns(3)
        for idx, item in enumerate(notes):
            with cols[idx % 3]:
                st.markdown(
                    f"""
                    <div class="sticky-note">
                        "{item['note']}"
                        <span class="sticky-name">— {item['name']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# ============================================================
# SECTION: SURPRISE BUTTON
# ============================================================
def render_surprise_button():
    """Render the big surprise button with confetti and celebratory message."""
    st.markdown('<div class="section-header">🎁 One Last <span>Surprise</span></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎁 Dad, Click Here!", use_container_width=True):
            st.session_state.surprise_clicked = True

    if st.session_state.surprise_clicked:
        st.balloons()
        st.snow()
        st.markdown(
            '<div class="surprise-msg">You are the world\'s best dad! 🏆❤️</div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.1)


# ============================================================
# SECTION: FOOTER
# ============================================================
def render_footer():
    """Render the closing footer message."""
    st.markdown(
        '<div class="footer">Made with ❤️ for the best Dad in the world.<br>'
        f"<span style='opacity:0.6; font-size:0.8rem;'>Father's Day {datetime.now().year}</span></div>",
        unsafe_allow_html=True,
    )


# ============================================================
# MAIN APP
# ============================================================
def main():
    """Main entry point — orchestrates rendering of all app sections."""
    load_css()
    render_floating_background()

    render_hero()
    st.markdown("---")
    render_personal_message()
    render_gallery()
    render_reasons()
    render_thank_you_wall()
    render_surprise_button()
    render_footer()


if __name__ == "__main__":
    main()
