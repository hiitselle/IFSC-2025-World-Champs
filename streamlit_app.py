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

# App title
st.header("🏆 Seoul World Champs 2025")

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
    df = load_data("https://docs.google.com/spreadsheets/d/1MYp0ek0L1XlZfDfcCWhgeMT97m2iJpmj7fk4Mj/export?format=csv&id=1d31J02E07")
elif genderSelect == "Female Boulder Semis":
    df = load_data("https://docs.google.com/spreadsheets/d/1MYp0ek0L1XlZfDfcCWhgeMT97m2iJpmj7fk4Mj/export?format=csv&id=1703E3211")
elif genderSelect == "Male Boulder Final":
    df = load_data("https://docs.google.com/spreadsheets/d/1MYp0ek0L1XlZfDfcCWhgeMT97m2iJpmj7fk4Mj/export?format=csv&id=1591B5873")
elif genderSelect == "Female Boulder Final":
    df = load_data("https://docs.google.com/spreadsheets/d/1MYp0ek0L1XlZfDfcCWhgeMT97m2iJpmj7fk4Mj/export?format=csv&id=1870E1337")
elif genderSelect == "Male Lead Semis":
    df = load_data("https://docs.google.com/spreadsheets/d/1MYp0ek0L1XlZfDfcCWhgeMT97m2iJpmj7fk4Mj/export?format=csv&id=1043E2777")
elif genderSelect == "Female Lead Semis":
    df = load_data("https://docs.google.com/spreadsheets/d/1MYp0ek0L1XlZfDfcCWhgeMT97m2iJpmj7fk4Mj/export?format=csv&id=1374E5433")
elif genderSelect == "Male Lead Final":
    df = load_data("https://docs.google.com/spreadsheets/d/1MYp0ek0L1XlZfDfcCWhgeMT97m2iJpmj7fk4Mj/export?format=csv&id=1497E4713")
elif genderSelect == "Female Lead Final":
    df = load_data("https://docs.google.com/spreadsheets/d/1MYp0ek0L1XlZfDfcCWhgeMT97m2iJpmj7fk4Mj/export?format=csv&id=1")

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

