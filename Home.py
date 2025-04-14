import streamlit as st
import time

# --- Page config ---
st.set_page_config(
    page_title="F1 Monza App",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# --- CSS Styling ---
st.markdown("""
    <style>
        .title-center {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            margin-top: 30px;
            margin-bottom: 0;
        }
        .subtitle-center {
            text-align: center;
            font-size: 20px;
            margin-top: 10px;
            margin-bottom: 40px;
            color: #aaa;
        }
        .icon-link {
            text-decoration: none;
            color: inherit;
        }
        .icon-block {
            margin-bottom: 40px;
        }
        .icon-emoji {
            font-size: 36px;
        }
        .icon-label {
            font-weight: bold;
            font-size: 20px;
            margin-top: 5px;
        }
        .icon-desc {
            font-size: 15px;
            color: #888;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title & Summary ---
st.markdown('<div class="title-center">🏁 F1 Monza Insights App</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-center">Explore the strategy, weather, and performance data from the 2024 Italian Grand Prix — all powered by interactive visuals and AI insights.</div>', unsafe_allow_html=True)

# --- Side-by-side layout: Image + Icons ---
left_col, right_col = st.columns([4, 1])  # Image gets ~80%, icons get ~20%


# Image on left
with left_col:
    st.image(r"C:\Users\sophi\OneDrive - Marquette University\Desktop - Copy\Spring 2025\AIM 4420\streamlit\monza.png", width=1400)

with right_col:
    st.markdown("<div style='font-size:36px; font-weight:bold;'>", unsafe_allow_html=True)
    st.page_link("pages/1_Dashboard.py", label="📊 Dashboard")
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("Visualize lap times, tire usage & performance.")

    st.markdown("<div style='font-size:30px; font-weight:bold;'>", unsafe_allow_html=True)
    st.page_link("pages/2_Chatbot.py", label="🤖 Chatbot")
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("Ask race questions and trace data-backed answers.")

    st.markdown("<div style='font-size:26px; font-weight:bold;'>", unsafe_allow_html=True)
    st.page_link("pages/3_Data_Editor.py", label="🧰 Data Editor")
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("Explore and adjust raw driver and timing data.")
