import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Streamlit setup
st.set_page_config(page_title="IFSC 2025 World Champs", layout="wide")

# Auto-refresh every 5 seconds
st.markdown("""
<script>
setTimeout(function(){
    window.location.reload();
}, 5000);
</script>
""", unsafe_allow_html=True)

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
@st.cache_data(ttl=5)  # Cache for only 5 seconds
def load_data(sheets_url):
    return pd.read_csv(sheets_url)

if genderSelect == "Male Boulder Semis":
    df = load_data("https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=911620167")
elif genderSelect == "Female Boulder Semis":
    df = load_data("https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=920221506")
elif genderSelect == "Male Boulder Final":
    df = load_data("https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=1415967322")
elif genderSelect == "Female Boulder Final":
    df = load_data("https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=299577805")
elif genderSelect == "Male Lead Semis":
    df = load_data("https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=0")
elif genderSelect == "Female Lead Semis":
    df = load_data("https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=352924417")
elif genderSelect == "Male Lead Final":
    df = load_data("https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=1091240908")
elif genderSelect == "Female Lead Final":
    df = load_data("https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=528108640")

# Ensure dataframe loaded
if df is None or df.empty:
    st.error("No data loaded for this round.")
    st.stop()

# Clean the data first with correct column names
# Handle both Lead and Boulder formats
if 'Points to 1st' in df.columns:
    df['Points to 1st'] = pd.to_numeric(df['Points to 1st'], errors='coerce').fillna('')
if 'Points to 2nd' in df.columns:
    df['Points to 2nd'] = pd.to_numeric(df['Points to 2nd'], errors='coerce').fillna('')
if 'Points to 3rd' in df.columns:
    df['Points to 3rd'] = pd.to_numeric(df['Points to 3rd'], errors='coerce').fillna('')
if 'Points for 1st Place' in df.columns:
    df['Points for 1st Place'] = pd.to_numeric(df['Points for 1st Place'], errors='coerce').fillna('')
if 'Points for 2nd Place' in df.columns:
    df['Points for 2nd Place'] = pd.to_numeric(df['Points for 2nd Place'], errors='coerce').fillna('')
if 'Points for 3rd Place' in df.columns:
    df['Points for 3rd Place'] = pd.to_numeric(df['Points for 3rd Place'], errors='coerce').fillna('')

# Create leaderboard with proper formatting (for sidebar - still sorted)
leaderboard_df = df.copy()

# Handle different ranking column names and create leaderboard
ranking_col = None
score_col = None
name_col = None

# Determine which columns to use based on what's available
if "Current Rank" in leaderboard_df.columns:
    ranking_col = "Current Rank"
elif "Current Position" in leaderboard_df.columns:
    ranking_col = "Current Position"

if "Manual Score" in leaderboard_df.columns:
    score_col = "Manual Score"
elif "Total Score" in leaderboard_df.columns:
    score_col = "Total Score"

if "Name" in leaderboard_df.columns:
    name_col = "Name"
elif "Athlete Name" in leaderboard_df.columns:
    name_col = "Athlete Name"

# Clean and convert ranking to numeric, then sort
if ranking_col and ranking_col in leaderboard_df.columns:
    leaderboard_df[ranking_col] = pd.to_numeric(leaderboard_df[ranking_col], errors='coerce')
    leaderboard_df = leaderboard_df.dropna(subset=[ranking_col])
    leaderboard_df = leaderboard_df.sort_values(by=ranking_col)

    # Format the ranking to show as integers
    leaderboard_df[ranking_col] = leaderboard_df[ranking_col].astype(int)

    # Select columns and get top 10
    cols_to_show = []
    if ranking_col: cols_to_show.append(ranking_col)
    if name_col: cols_to_show.append(name_col)
    if score_col: cols_to_show.append(score_col)
    
    leaderboard = leaderboard_df[cols_to_show].head(10)
else:
    # Fallback if no ranking column found
    leaderboard = pd.DataFrame({"Info": ["No ranking data available"]})

st.sidebar.table(leaderboard)  # Top 10

# --- Main Page (Existing Athlete Cards) ---
st.title("🏆 Seoul World Champs 2025")

# ---- Athlete Info Card Function ----
def generateInfo(x):
    row = df.iloc[x]

    # Handle ranking display - check for different ranking column names
    rank_val = row.get("Current Rank", row.get("Current Position", ""))
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

    # Get data using correct column names from the sheet - handle both formats
    name = safe_get_value('Name') if 'Name' in row else safe_get_value('Athlete Name')
    
    # Handle different score column names
    total_score = safe_get_value('Manual Score') if 'Manual Score' in row else safe_get_value('Total Score')
    
    # Boulder-specific columns
    boulder_1_score = safe_get_value('Boulder 1 Score')
    boulder_2_score = safe_get_value('Boulder 2 Score') 
    boulder_3_score = safe_get_value('Boulder 3 Score')
    boulder_4_score = safe_get_value('Boulder 4 Score')
    
    # Points columns - handle both formats
    points_to_1st = safe_get_value('Points to 1st') if 'Points to 1st' in row else safe_get_value('Points for 1st Place')
    points_to_2nd = safe_get_value('Points to 2nd') if 'Points to 2nd' in row else safe_get_value('Points for 2nd Place')
    points_to_3rd = safe_get_value('Points to 3rd') if 'Points to 3rd' in row else safe_get_value('Points for 3rd Place')
    
    # Other columns
    worst_finish = safe_get_value('Worst Finish') if 'Worst Finish' in row else safe_get_value('Worst Possible Finish')
    min_to_qualify = safe_get_value('Min to Qualify') if 'Min to Qualify' in row else safe_get_value('Points Needed for Top 8')

    # Handle qualification status - different column names
    status = str(row.get("Status", "")).strip().lower()
    if not status:
        # Check for alternative status indicators
        if "qualified" in str(row.get("Status", "")).lower():
            status = "qualified"
        elif "eliminated" in str(row.get("Status", "")).lower():
            status = "eliminated"
        elif "still in contention" in str(row.get("Status", "")).lower():
            status = "still in contention"

    if "qualified" in status and "eliminated" not in status:
        badge = "🟢 Qualified"
        bg_color = "#d4edda"  # Light green background
        border_color = "#28a745"  # Green border
        text_color = "#155724"  # Dark green text
    elif "eliminated" in status:
        badge = "🔴 Eliminated"
        bg_color = "#f8d7da"  # Light red background
        border_color = "#dc3545"  # Red border
        text_color = "#721c24"  # Dark red text
    elif "still in contention" in status:
        badge = "🟡 Still in Contention"
        bg_color = "#fff3cd"  # Light yellow background
        border_color = "#ffc107"  # Yellow border
        text_color = "#856404"  # Dark yellow text
    else:
        badge = f"❓ {status}"
        bg_color = "#ffffff"  # White background
        border_color = "#cccccc"  # Gray border
        text_color = "#000000"  # Black text

    # Build the info card HTML - adapt to show relevant data
    score_info = ""
    if total_score != 'N/A':
        score_info += f"<p style='color:{text_color};'><b>Total Score:</b> {total_score}</p>"
    
    # Show boulder scores if available
    if boulder_1_score != 'N/A' or boulder_2_score != 'N/A':
        score_info += f"<p style='color:{text_color};'><b>Boulder Scores:</b> {boulder_1_score}, {boulder_2_score}, {boulder_3_score}, {boulder_4_score}</p>"
    
    points_info = ""
    if points_to_1st != 'N/A':
        points_info += f"<p style='color:{text_color};'><b>Points to 1st:</b> {points_to_1st}</p>"
    if points_to_2nd != 'N/A':
        points_info += f"<p style='color:{text_color};'><b>Points to 2nd:</b> {points_to_2nd}</p>"
    if points_to_3rd != 'N/A':
        points_info += f"<p style='color:{text_color};'><b>Points to 3rd:</b> {points_to_3rd}</p>"
    
    additional_info = ""
    if worst_finish != 'N/A':
        additional_info += f"<p style='color:{text_color};'><b>Worst Finish:</b> {worst_finish}</p>"
    if min_to_qualify != 'N/A':
        additional_info += f"<p style='color:{text_color};'><b>Min to Qualify:</b> {min_to_qualify}</p>"

    st.markdown(
        f"""
        <div style="background-color:{bg_color}; color:{text_color}; border:2px solid {border_color}; border-radius:15px; padding:20px; box-shadow: 4px 4px 10px rgba(0,0,0,0.1); margin:10px 0;">
            <h2 style="margin-bottom:5px; color:{text_color};">#{rank_display} {name}</h2>
            {score_info}
            {points_info}
            {additional_info}
            <p style="color:{text_color};"><b>Status:</b> {badge}</p>
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

# ---- Athlete Selector with Ranking (ORIGINAL SPREADSHEET ORDER) ----
st.title("👟 Athlete Rankings")

# Create athletes list in ORIGINAL spreadsheet order (no sorting)
athletes_display = []

# Determine column names safely
name_col = None
rank_col = None

if 'Name' in df.columns:
    name_col = 'Name'
elif 'Athlete Name' in df.columns:
    name_col = 'Athlete Name'

if 'Current Rank' in df.columns:
    rank_col = 'Current Rank'
elif 'Current Position' in df.columns:
    rank_col = 'Current Position'

if name_col:
    for index, row in df.iterrows():
        name = row.get(name_col, '')
        if pd.notna(name) and str(name).strip() != "":
            rank_val = row.get(rank_col, "") if rank_col else ""
            if pd.isna(rank_val) or rank_val == '':
                rank_display = "-"
            else:
                try:
                    rank_display = str(int(float(rank_val)))
                except (ValueError, TypeError):
                    rank_display = str(rank_val)
            
            athletes_display.append(f"{rank_display}. {name}")

    if athletes_display:
        selected_display = st.selectbox("Select an athlete", athletes_display)
        if selected_display:
            # Extract name from the selected display string
            if ". " in selected_display:
                selected_name = selected_display.split(". ", 1)[1]
            else:
                selected_name = selected_display
                
            # Find the athlete in the original df to get their original index
            original_athlete_row = df[df[name_col] == selected_name]
            if not original_athlete_row.empty:
                selected_row = original_athlete_row.iloc[0]
                original_index = original_athlete_row.index[0]

                # Show athlete card
                if rank_col:
                    ranking = pd.to_numeric(selected_row[rank_col], errors='coerce')
                    if pd.notna(ranking):
                        st.subheader(f"{selected_row[name_col]} — #{int(ranking)}")
                    else:
                        st.subheader(f"{selected_row[name_col]}")
                else:
                    st.subheader(f"{selected_row[name_col]}")
                generateInfo(original_index)
else:
    st.write("No athlete data available.")

# ---- Expanders with all athletes (sorted by actual ranking) ----
st.subheader("📋 All Athletes")

# Create a copy for sorting by ranking
df_for_expanders = df.copy()

# Determine column names safely
name_col = None
rank_col = None

if 'Name' in df_for_expanders.columns:
    name_col = 'Name'
elif 'Athlete Name' in df_for_expanders.columns:
    name_col = 'Athlete Name'

if 'Current Rank' in df_for_expanders.columns:
    rank_col = 'Current Rank'
elif 'Current Position' in df_for_expanders.columns:
    rank_col = 'Current Position'

if name_col:
    if rank_col:
        df_for_expanders[rank_col] = pd.to_numeric(df_for_expanders[rank_col], errors='coerce')
        
        # Separate athletes with and without rankings
        athletes_with_ranking = df_for_expanders[df_for_expanders[rank_col].notna()].sort_values(by=rank_col)
        athletes_without_ranking = df_for_expanders[df_for_expanders[rank_col].isna()]
        
        # Show athletes with rankings first (in ranking order)
        for original_index, row in athletes_with_ranking.iterrows():
            name = row[name_col]
            ranking = int(row[rank_col])
            if pd.isna(name) or str(name).strip() == "":
                name = f"Athlete {original_index+1}"
            
            # Check status to style the expander header
            status = str(row.get("Status", "")).strip().lower()
            if "qualified" in status and "eliminated" not in status:
                expander_label = f"🟢 #{ranking} - {name}"
            elif "eliminated" in status:
                expander_label = f"🔴 #{ranking} - {name}"
            elif "still in contention" in status:
                expander_label = f"🟡 #{ranking} - {name}"
            else:
                expander_label = f"#{ranking} - {name}"
            
            with st.expander(expander_label):
                generateInfo(original_index)
        
        # Show athletes without rankings last
        for original_index, row in athletes_without_ranking.iterrows():
            name = row[name_col]
            if pd.isna(name) or str(name).strip() == "":
                name = f"Athlete {original_index+1}"
            
            # Check status to style the expander header
            status = str(row.get("Status", "")).strip().lower()
            if "qualified" in status and "eliminated" not in status:
                expander_label = f"🟢 Unranked - {name}"
            elif "eliminated" in status:
                expander_label = f"🔴 Unranked - {name}"
            elif "still in contention" in status:
                expander_label = f"🟡 Unranked - {name}"
            else:
                expander_label = f"Unranked - {name}"
            
            with st.expander(expander_label):
                generateInfo(original_index)
    else:
        # No ranking column, just show all athletes
        for original_index, row in df_for_expanders.iterrows():
            name = row.get(name_col, '')
            if pd.notna(name) and str(name).strip() != "":
                status = str(row.get("Status", "")).strip().lower()
                if "qualified" in status and "eliminated" not in status:
                    expander_label = f"🟢 {name}"
                elif "eliminated" in status:
                    expander_label = f"🔴 {name}"
                elif "still in contention" in status:
                    expander_label = f"🟡 {name}"
                else:
                    expander_label = f"{name}"
                
                with st.expander(expander_label):
                    generateInfo(original_index)
else:
    st.write("No athlete data available.")

st.write("Made by Elle ✨")
