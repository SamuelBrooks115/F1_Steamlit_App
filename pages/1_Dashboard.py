import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from theme_utils import apply_theme


# --- Page Config ---
st.set_page_config(page_title="Dashboard | F1 Monza", page_icon="🏎️", layout="wide")
apply_theme()


# --- Global CSS Font Injection ---
st.markdown("""
    <style>
        h1 { font-size: 36px !important; }
        h2 { font-size: 30px !important; }
        h3 { font-size: 26px !important; }
        h4 { font-size: 22px !important; }
        p, li, .markdown-text-container {
            font-size: 18px !important;
            line-height: 1.6;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏎️ Monza 2024 F1 Dashboard")
st.markdown("## Your command center for the 2024 Italian Grand Prix. Dive into real-time weather data, driver strategy, lap performance, and race results — all in one dynamic dashboard.")


# --- Load Excel Data ---
@st.cache_data
def load_data():
    excel_file = pd.ExcelFile("data/monza_data.xlsx")
    pit_df = pd.read_excel(excel_file, sheet_name=0)
    weather_df = pd.read_excel(excel_file, sheet_name=1)
    messages_df = pd.read_excel(excel_file, sheet_name=2)
    return pit_df, weather_df, messages_df

pit_df, weather_df, messages_df = load_data()

# --- Connect to SQLite DB ---
try:
    conn = sqlite3.connect("data/Structured_Data.db")
except Exception as e:
    st.error(f"❌ Database connection failed: {e}")
    st.stop()

# --- WEATHER SECTION ---
st.markdown("## 🌤️ Weather Data")
with st.expander("View Weather Details", expanded=False):
    st.markdown("#### Weather Snapshot")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Avg Track Temp (°C)", f"{weather_df['TrackTemp'].mean():.1f}")
    kpi2.metric("Avg Wind Speed (km/h)", f"{weather_df['WindSpeed'].mean():.1f}")
    kpi3.metric("Total Rainfall (mm)", f"{weather_df['Rainfall'].sum():.1f}")

    st.markdown("<br><hr style='border-top: 2px solid white; margin: 30px 0;'><br>", unsafe_allow_html=True)

    st.markdown("#### 🔥 Track Temperature Trend")
    fig_temp = px.line(weather_df, x="Time", y="TrackTemp", markers=True,
                       title="Track Temperature Over Time")
    st.plotly_chart(fig_temp, use_container_width=True)

    st.markdown("<br><hr style='border-top: 2px solid white; margin: 30px 0;'><br>", unsafe_allow_html=True)

    st.markdown("#### 💨 Wind Analysis")
    wind_options = sorted(weather_df["WindDirection"].dropna().unique())
    selected_wind = st.selectbox("Select Wind Direction", wind_options)
    filtered_wind = weather_df[weather_df["WindDirection"] == selected_wind]
    st.dataframe(filtered_wind)

# --- RACE RESULTS SECTION ---
st.markdown("## 🏎️ Race Results")
with st.expander("View Race Results", expanded=False):
    st.markdown("#### 🌟 Driver Insights")
    driver_info_df = pd.read_sql_query("SELECT DriverID, FullName FROM Driver", conn)
    driver_names = sorted(driver_info_df["FullName"].dropna().unique())
    selected_driver_name = st.selectbox("Select a Driver", driver_names)
    driver_id = driver_info_df.loc[driver_info_df["FullName"] == selected_driver_name, "DriverID"].iloc[0]

    view_option = st.selectbox("Select Data to View", ["🏎️ Qualifying Times", "🏅 Race Result"])

    if view_option == "🏎️ Qualifying Times":
        qual_query = "SELECT Q1, Q2, Q3 FROM QualifyingResults WHERE DriverID = ?"
        qual_df = pd.read_sql_query(qual_query, conn, params=(driver_id,))
        if not qual_df.empty:
            st.table(qual_df)
        else:
            st.warning("No qualifying data available for this driver.")

    elif view_option == "🏅 Race Result":
        race_query = "SELECT Position, GridPosition, Points FROM RaceResults WHERE DriverID = ?"
        race_df = pd.read_sql_query(race_query, conn, params=(driver_id,))
        if not race_df.empty:
            st.table(race_df)
        else:
            st.warning("No race result data available for this driver.")

    st.markdown("<br><hr style='border-top: 2px solid white; margin: 30px 0;'><br>", unsafe_allow_html=True)

    st.markdown("#### 🧮 Points Leaderboard")
    points_query = """
        SELECT d.FullName, SUM(r.Points) AS TotalPoints
        FROM RaceResults r
        JOIN Driver d ON r.DriverID = d.DriverID
        GROUP BY d.FullName
        ORDER BY TotalPoints DESC
    """
    points_df = pd.read_sql_query(points_query, conn)
    if not points_df.empty:
        fig_points = px.bar(points_df, x="FullName", y="TotalPoints", title="Total Points by Driver")
        st.plotly_chart(fig_points, use_container_width=True)

    st.markdown("<br><hr style='border-top: 2px solid white; margin: 30px 0;'><br>", unsafe_allow_html=True)

    st.markdown("#### ⚡ Fastest Lap Per Driver")
    fastest_lap_query = """
        SELECT d.FullName, MIN(td.LapTime) AS FastestLap
        FROM TimingData td
        JOIN Driver d ON td.DriverID = d.DriverNumber
        GROUP BY d.FullName
        ORDER BY FastestLap ASC
    """
    fastest_lap_df = pd.read_sql_query(fastest_lap_query, conn)
    if not fastest_lap_df.empty:
        fig_laps = px.bar(fastest_lap_df, x="FullName", y="FastestLap", title="Fastest Laps by Driver")
        st.plotly_chart(fig_laps, use_container_width=True)

# --- STRATEGY + LAP TIMES SECTION ---
st.markdown("## 🔍 Strategy & Lap Times")
with st.expander("View Lap Analysis", expanded=False):
    st.markdown("#### 🔁 Tire Usage by Compound and Driver")
    compound_query = """
        SELECT d.FullName, td.Compound, COUNT(*) AS LapsUsed
        FROM TimingData td
        JOIN Driver d ON td.DriverID = d.DriverNumber
        WHERE td.Compound IS NOT NULL
        GROUP BY d.FullName, td.Compound
    """
    compound_df = pd.read_sql_query(compound_query, conn)
    if not compound_df.empty:
        fig_comp = px.bar(compound_df, x="FullName", y="LapsUsed", color="Compound",
                          title="Tire Usage by Compound and Driver", barmode="stack")
        st.plotly_chart(fig_comp, use_container_width=True)

    st.markdown("<br><hr style='border-top: 2px solid white; margin: 30px 0;'><br>", unsafe_allow_html=True)

    st.markdown("#### 📈 Lap Time Trend by Driver")
    lap_driver_query = """
        SELECT DISTINCT d.FullName
        FROM TimingData td
        JOIN Driver d ON td.DriverID = d.DriverNumber
    """
    lap_driver_names = pd.read_sql_query(lap_driver_query, conn)["FullName"].tolist()
    selected_lap_driver = st.selectbox("Select Driver to View Lap Times", lap_driver_names)

    lap_data_query = """
        SELECT td.LapNumber, td.LapTime
        FROM TimingData td
        JOIN Driver d ON td.DriverID = d.DriverNumber
        WHERE d.FullName = ?
        ORDER BY td.LapNumber ASC
    """
    lap_data_df = pd.read_sql_query(lap_data_query, conn, params=(selected_lap_driver,))
    if not lap_data_df.empty:
        lap_data_df["LapTime"] = pd.to_timedelta(lap_data_df["LapTime"])
        lap_data_df["LapSeconds"] = lap_data_df["LapTime"].dt.total_seconds()

        def format_timedelta(td):
            total_sec = td.total_seconds()
            minutes = int(total_sec // 60)
            seconds = total_sec % 60
            return f"{minutes}:{seconds:06.3f}"

        lap_data_df["LapFormatted"] = lap_data_df["LapTime"].apply(format_timedelta)

        st.markdown(f"#### {selected_lap_driver} - Per-Lap Times")
        fig_lap = px.line(
            lap_data_df,
            x="LapNumber",
            y="LapSeconds",
            title=f"Lap Times for {selected_lap_driver}",
            markers=True,
            labels={"LapSeconds": "Lap Time (s)"}
        )
        st.plotly_chart(fig_lap, use_container_width=True)

        if st.toggle("📃 Show Per-Lap Times Table"):
            st.dataframe(lap_data_df[["LapNumber", "LapFormatted"]])
