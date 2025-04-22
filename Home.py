import streamlit as st
import time
from theme_utils import apply_theme

# --- Page config ---
st.set_page_config(
    page_title="F1 Monza App",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Team Theme Selector ---
st.sidebar.markdown("## 🎨 Choose Your Team Theme")

# Initialize or persist team theme
if "team_theme" not in st.session_state:
    st.session_state.team_theme = "Default"

team_theme = st.sidebar.selectbox(
    "Select a Team",
    ["Default", "Ferrari", "Mercedes", "Red Bull", "McLaren", "Alpine","Williams", "Racing Bulls","Haas", "Aston Martin","Kick Sauber"],
    index=["Default", "Ferrari", "Mercedes", "Red Bull", "McLaren", "Alpine","Williams", "Racing Bulls","Haas", "Aston Martin","Kick Sauber"].index(st.session_state.team_theme),
    key="team_theme"
)

apply_theme()

# --- Loading Screen ---
def show_loading_screen():
    placeholder = st.empty()
    with placeholder.container():
        with st.spinner("Loading your personalized dashboard..."):
            st.markdown("""
                <style>
                .loading-img {
                    display: flex;
                    justify-content: center;
                    margin-top: 50px;
                }
                </style>
                <div class='loading-img'>
                    <img src='https://media.giphy.com/media/qXyo3Yf1XW64o/giphy.gif' width='300'>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(2)
    placeholder.empty()

show_loading_screen()

# --- Title & Summary ---
st.title("🏁 F1 Monza Insights App")
st.markdown(
    '<div class="subtitle-center">Explore the strategy, weather, and performance data from the 2024 Italian Grand Prix — all powered by interactive visuals and AI insights.</div>',
    unsafe_allow_html=True
)

# --- Side-by-side layout: Image + Icons ---
left_col, right_col = st.columns([4, 1])

with left_col:
    st.image(r"C:\Users\samue\OneDrive\Desktop\Local Folder\F1_Steamlit_App#\monza.png", width=1400)

with right_col:
    st.markdown("<div style='font-size:36px; font-weight:bold;'>", unsafe_allow_html=True)
    st.page_link("pages/1_Dashboard.py", label="📊 Dashboard")
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("Visualize lap times, tire usage & performance.")

    st.markdown("<div style='font-size:100px; font-weight:bold;'>", unsafe_allow_html=True)
    st.page_link("pages/2_Chatbot.py", label="🤖 Chatbot")
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("Ask race questions and trace data-backed answers.")

    st.markdown("<div style='font-size:26px; font-weight:bold;'>", unsafe_allow_html=True)
    st.page_link("pages/3_Data_Editor.py", label="🧰 Data Editor")
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("Explore and adjust raw driver and timing data.")
