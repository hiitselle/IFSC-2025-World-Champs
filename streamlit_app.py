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

# Ensure dataframe loaded
if df is None or df.empty:
    st.error("No data loaded for this round.")
    st.stop()

# Clean the data first with correct column names
if 'Points to 1st na' in df.columns:
    df['Points to 1st na'] = pd.to_numeric(df['Points to 1st na'], errors='coerce').fillna('')
if 'Points to 2nd na' in df.columns:
    df['Points to 2nd na'] = pd.to_numeric(df['Points to 2nd na'], errors='coerce').fillna('')
if 'Points to 3rd na' in df.columns:
    df['Points to 3rd na'] = pd.to_numeric(df['Points to 3rd na'], errors='coerce').fillna('')

# Create leaderboard with proper formatting
leaderboard_df = df.copy()

# Clean and convert ranking to numeric, then sort
leaderboard_df["Actual Ranking"] = pd.to_numeric(leaderboard_df["Actual Ranking"], errors='coerce')
leaderboard_df = leaderboard_df.dropna(subset=["Actual Ranking"])
leaderboard_df = leaderboard_df.sort_values(by="Actual Ranking")

# Format the ranking to show as integers
leaderboard_df["Actual Ranking"] = leaderboard_df["Actual Ranking"].astype(int)

# Select columns and get top 10
leaderboard = leaderboard_df[["Actual Ranking", "Name", "TotalScore"]].head(10)

st.sidebar.table(leaderboard)  # Top 10

# --- Main Page (Existing Athlete Cards) ---
st.title("🏆 Seoul World Champs 2025")

# ---- Athlete Info Card Function ----
def generateInfo(x):
    row = df.iloc[x]

    # Handle ranking display
    rank_val = row.get("Actual Ranking", "")
    if pd.isna(rank_val) or rank_val == '':
        rank_display = "-"
    else:
        try:
            rank_display = str(int(float(rank_val)))
        except (ValueError, TypeError):
            rank_display = str(rank_val)

    # Handle data safely with correct column names
    def safe_get_value(column_name):
        val = row.get(column_name, '')
        if pd.isna(val) or val == '':
            return 'N/A'
        return str(val)

    # Get data using correct column names from the sheet
    name = safe_get_value('Name')
    total_score = safe_get_value('TotalScore')
    boulder_score = safe_get_value('BoulderScore')
    route_score = safe_get_value('RouteScore')
    points_to_1st = safe_get_value('Points to 1st na')
    points_to_2nd = safe_get_value('Points to 2nd na') 
    points_to_3rd = safe_get_value('Points to 3rd na')
    worst_case = safe_get_value('Worst Case')

    qualified = str(row.get("Qualified", "")).strip().lower()
    if qualified in ["qualified", "true", "1"]:
        badge = "🟢 Qualified"
    elif qualified in ["not qualified", "false", "0"]:
        badge = "🔴 Not Qualified"
    else:
        badge = f"❓ {qualified}"

    st.markdown(
        f"""
        <div style="background-color:#ffffff; color:#000000; border-radius:15px; padding:20px; box-shadow: 4px 4px 10px rgba(0,0,0,0.1); margin:10px 0;">
            <h2 style="margin-bottom:5px; color:#000000;">#{rank_display} {name}</h2>
            <p style="color:#000000;"><b>Total Score:</b> {total_score}</p>
            <p style="color:#000000;"><b>Boulder Score:</b> {boulder_score}</p>
            <p style="color:#000000;"><b>Route Score:</b> {route_score}</p>
            <p style="color:#000000;"><b>Points to 1st:</b> {points_to_1st}</p>
            <p style="color:#000000;"><b>Points to 2nd:</b> {points_to_2nd}</p>
            <p style="color:#000000;"><b>Points to 3rd:</b> {points_to_3rd}</p>
            <p style="color:#000000;"><b>Worst Case:</b> {worst_case}</p>
            <p style="color:#000000;"><b>Status:</b> {badge}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div style="background-color:#f9f9f9; border-radius:15px; padding:20px;">
        <h3>Competition Info</h3>
        <ul>
            <li>Top 1: Qualified </li>
            <li>Top 2: Needs Top to Qualify</li>
            <li>Top 3: Needs Zone (Fewer Tops)</li>
            <li>Top 4: Needs Zone and Tops</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# ---- Athlete Selector with Ranking ----
st.title("💟 Athlete Rankings")

# Create a sorted version for the selector (but don't modify the original df)
df_sorted = df.copy()
df_sorted['Actual Ranking'] = pd.to_numeric(df_sorted['Actual Ranking'], errors='coerce')
df_sorted = df_sorted.dropna(subset=['Actual Ranking'])
df_sorted = df_sorted.sort_values(by='Actual Ranking')

athletes_display = [
    f"{int(row['Actual Ranking'])}. {row['Name']}"
    for _, row in df_sorted.iterrows()
    if pd.notna(row['Actual Ranking']) and str(row['Name']).strip() != ""
]

if athletes_display:
    selected_display = st.selectbox("Select an athlete", athletes_display)
    if selected_display:
        selected_name = selected_display.split(". ", 1)[1]
        # Find the athlete in the original df to get their original index
        original_athlete_row = df[df['Name'] == selected_name]
        if not original_athlete_row.empty:
            selected_row = original_athlete_row.iloc[0]
            original_index = original_athlete_row.index[0]

            # Show athlete card
            ranking = pd.to_numeric(selected_row['Actual Ranking'], errors='coerce')
            if pd.notna(ranking):
                st.subheader(f"{selected_row['Name']} — #{int(ranking)}")
            else:
                st.subheader(f"{selected_row['Name']}")
            generateInfo(original_index)

# ---- Expanders with all athletes (in original spreadsheet order) ----
st.subheader("📋 All Athletes")
for x in range(len(df)):
    name = df["Name"].iloc[x]
    if pd.isna(name) or str(name).strip() == "":
        name = f"Athlete {x+1}"
    
    with st.expander(str(name)):
        generateInfo(x)

st.write("Made by Elle ✨")

