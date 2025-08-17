import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Streamlit setup
st.set_page_config(page_title="IFSC 2025 World Champs", layout="wide")
st_autorefresh = st.experimental_memo

# Background + styling
st.markdown("""
<style>
div[data-testid="stAppViewContainer"] {
    background-color: #222;
    color: white;
}
header[data-testid="stHeader"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# Sidebar round selector
with st.sidebar:
    genderSelect = st.selectbox(
        "Select Round",
        [
            "Male Boulder Semis", "Female Boulder Semis",
            "Male Boulder Final", "Female Boulder Final",
            "Male Lead Semis", "Female Lead Semis",
            "Male Lead Final", "Female Lead Final"
        ]
    )

# Load data from Google Sheets
@st.cache_data(ttl=600)
def load_data(sheets_url):
    return pd.read_csv(sheets_url)

if genderSelect == "Male Boulder Semis":
    df = load_data("https://docs.google.com/spreadsheets/d/1RVgQboeDCi1X2zEQdCzWqe9HYQTJpj5EumjFXf4qjN0/export?format=csv&gid=1631360020")
elif genderSelect == "Female Boulder Semis":
    df = load_data("https://docs.google.com/spreadsheets/d/1RVgQboeDCi1X2zEQdCzWqe9HYQTJpj5EumjFXf4qjN0/export?format=csv&gid=1785852811")
elif genderSelect == "Male Boulder Final":
    df = load_data("https://docs.google.com/spreadsheets/d/1RVgQboeDCi1X2zEQdCzWqe9HYQTJpj5EumjFXf4qjN0/export?format=csv&gid=935198785")
elif genderSelect == "Female Boulder Final":
    df = load_data("https://docs.google.com/spreadsheets/d/1RVgQboeDCi1X2zEQdCzWqe9HYQTJpj5EumjFXf4qjN0/export?format=csv&gid=769323139")
elif genderSelect == "Male Lead Semis":
    df = load_data("https://docs.google.com/spreadsheets/d/1RVgQboeDCi1X2zEQdCzWqe9HYQTJpj5EumjFXf4qjN0/export?format=csv&gid=1842627779")
elif genderSelect == "Female Lead Semis":
    df = load_data("https://docs.google.com/spreadsheets/d/1RVgQboeDCi1X2zEQdCzWqe9HYQTJpj5EumjFXf4qjN0/export?format=csv&gid=137564533")
elif genderSelect == "Male Lead Final":
    df = load_data("https://docs.google.com/spreadsheets/d/1RVgQboeDCi1X2zEQdCzWqe9HYQTJpj5EumjFXf4qjN0/export?format=csv&gid=0")
elif genderSelect == "Female Lead Final":
    df = load_data("https://docs.google.com/spreadsheets/d/1RVgQboeDCi1X2zEQdCzWqe9HYQTJpj5EumjFXf4qjN0/export?format=csv&gid=1947247931")

leaderboard = df.sort_values(by="Actual Ranking")[
    ["Actual Ranking", "Name", "TotalScore"]
]
st.sidebar.table(leaderboard.head(10))  # Top 10

# --- Main Page (Existing Athlete Cards) ---
st.title("🏆 Seoul World Champs 2025")

for x in range(len(df)):
    # OLD (causing TypeError)
    # with st.expander(df["Name"].iloc[x]):

    # NEW (safe)
    name = df["Name"].iloc[x]
    if pd.isna(name):
        name = f"Athlete {x+1}"
    with st.expander(str(name)):

row = df.iloc[x]

# safely handle Actual Ranking
rank_val = row.get("Actual Ranking", 0)
try:
    rank_val = int(float(rank_val))
except (ValueError, TypeError):
    rank_val = 0

st.markdown(
    f"""
    <div style="background-color:#f9f9f9; border-radius:15px; padding:20px; box-shadow: 4px 4px 10px rgba(0,0,0,0.1)">
        <h2 style="margin-bottom:5px;">{rank_val}. {row.get('Name','')}</h2>
        <p><b>Total Score:</b> {row.get('TotalScore','')}</p>
        <p><b>Points to 1st:</b> {row.get('Points to 1st','')}</p>
        <p><b>Points to 2nd:</b> {row.get('Points to 2nd','')}</p>
        <p><b>Points to 3rd:</b> {row.get('Points to 3rd','')}</p>
        <p><b>Min holds to Q:</b> {row.get('Min Hold to Qualify','')}</p>
    </div>
    """,
    unsafe_allow_html=True
)





# Ensure dataframe loaded
if df is None or df.empty:
    st.error("No data loaded for this round.")
    st.stop()

# ---- Athlete Info Card Function ----
def generateInfo(x):
    row = df.iloc[x]

    qualified = str(row.get("Qualified", "")).strip().lower()
    if qualified in ["yes", "true", "1"]:
        badge = "🟢 Qualified"
    else:
        badge = "🔴 Not Qualified"

    st.markdown(
        f"""
        <div style="background-color:#f9f9f9; border-radius:15px; padding:20px;
                    box-shadow: 4px 4px 10px rgba(0,0,0,0.1); color:black;">
            <h2 style="margin-bottom:5px;">{int(row.get('Actual Ranking', 0))}. {row.get('Name','')}</h2>
            <p><b>{badge}</b></p>
            <p><b>Total Score:</b> {row.get('TotalScore','')}</p>
            <p><b>Points to 1st:</b> {row.get('Points to 1st','')}</p>
            <p><b>Points to 2nd:</b> {row.get('Points to 2nd','')}</p>
            <p><b>Points to 3rd:</b> {row.get('Points to 3rd','')}</p>
            <p><b>Min Needed:</b> {row.get('Min needed','')}</p>
            <p><b>Min Hold to Qualify:</b> {row.get('Min Hold to Qualify','')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---- Athlete Selector with Ranking ----
st.title("👟 Athlete Rankings")

df['Actual Ranking'] = pd.to_numeric(df['Actual Ranking'], errors='coerce')
df = df.dropna(subset=['Actual Ranking'])
df = df.sort_values(by='Actual Ranking')

athletes_display = [
    f"{int(row['Actual Ranking'])}. {row['Name']}"
    for _, row in df.iterrows()
    if pd.notna(row['Actual Ranking']) and str(row['Name']).strip() != ""
]

selected_display = st.selectbox("Select an athlete", athletes_display)
if selected_display:
    selected_name = selected_display.split(". ", 1)[1]
    selected_row = df[df['Name'] == selected_name].iloc[0]

    # Show athlete card
    st.subheader(f"{selected_row['Name']} — #{int(selected_row['Actual Ranking'])}")
    generateInfo(df[df['Name'] == selected_name].index[0])

# ---- Expanders with all athletes ----
st.subheader("📋 All Athletes")
for x in range(len(df)):
    with st.expander(df["Name"].iloc[x]):
        generateInfo(x)

st.write("Made by Elle ✨")

