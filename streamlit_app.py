import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Configuration
SHEETS_URLS = {
    "Male Boulder Semis": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=911620167",
    "Female Boulder Semis": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=920221506",
    "Male Boulder Final": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=1415967322",
    "Female Boulder Final": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=299577805",
    "Male Lead Semis": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=0",
    "Female Lead Semis": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=352924417",
    "Male Lead Final": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=1091240908",
    "Female Lead Final": "https://docs.google.com/spreadsheets/d/1MwVp1mBUoFrzRSIIu4UdMcFlXpxHAi_R7ztp1E4Vgx0/export?format=csv&gid=528108640"
}

def setup_page():
    """Configure Streamlit page settings and styling"""
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

@st.cache_data(ttl=5)
def load_data(sheets_url):
    """Load data from Google Sheets with caching"""
    return pd.read_csv(sheets_url)

def clean_data(df):
    """Clean and standardize dataframe columns"""
    # Clean points columns
    points_columns = [
        'Points to 1st', 'Points to 2nd', 'Points to 3rd',
        'Points for 1st Place', 'Points for 2nd Place', 'Points for 3rd Place'
    ]
    
    for col in points_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna('')
    
    return df

def get_column_names(df):
    """Determine which column names to use based on available columns"""
    # Name column
    name_col = None
    for col in ['Name', 'Athlete Name', 'name', 'athlete_name']:
        if col in df.columns:
            name_col = col
            break
    
    # Rank column  
    rank_col = None
    for col in ['Current Rank', 'Current Position', 'Rank', 'Position', 'rank', 'position']:
        if col in df.columns:
            rank_col = col
            break
    
    # Score column
    score_col = None
    for col in ['Manual Score', 'Total Score', 'Score', 'score', 'total_score']:
        if col in df.columns:
            score_col = col
            break
    
    return name_col, rank_col, score_col

def create_leaderboard(df, name_col, rank_col, score_col):
    """Create top 10 leaderboard for sidebar"""
    if df.empty or name_col is None:
        return pd.DataFrame({"Info": ["No data available"]})
    
    leaderboard_df = df.copy()
    
    if rank_col and rank_col in leaderboard_df.columns:
        leaderboard_df[rank_col] = pd.to_numeric(leaderboard_df[rank_col], errors='coerce')
        leaderboard_df = leaderboard_df.dropna(subset=[rank_col])
        
        if not leaderboard_df.empty:
            leaderboard_df = leaderboard_df.sort_values(by=rank_col)
            leaderboard_df[rank_col] = leaderboard_df[rank_col].astype(int)
            
            # Select only available columns
            cols_to_show = []
            if rank_col: cols_to_show.append(rank_col)
            if name_col: cols_to_show.append(name_col)
            if score_col and score_col in leaderboard_df.columns: cols_to_show.append(score_col)
            
            return leaderboard_df[cols_to_show].head(10)
    
    return pd.DataFrame({"Info": ["No ranking data available"]})

def get_status_styling(status):
    """Return styling based on athlete status"""
    status = str(status).strip().lower()
    
    if "qualified" in status and "eliminated" not in status:
        return {
            'badge': "🟢 Qualified",
            'bg_color': "#d4edda",
            'border_color': "#28a745",
            'text_color': "#155724"
        }
    elif "eliminated" in status:
        return {
            'badge': "🔴 Eliminated", 
            'bg_color': "#f8d7da",
            'border_color': "#dc3545",
            'text_color': "#721c24"
        }
    elif "still in contention" in status:
        return {
            'badge': "🟡 Still in Contention",
            'bg_color': "#fff3cd",
            'border_color': "#ffc107", 
            'text_color': "#856404"
        }
    else:
        return {
            'badge': f"❓ {status}",
            'bg_color': "#ffffff",
            'border_color': "#cccccc",
            'text_color': "#000000"
        }

def safe_get_value(row, column_name):
    """Safely get value from row, handling missing data"""
    val = row.get(column_name, '')
    return 'N/A' if pd.isna(val) or val == '' else str(val)

def generate_athlete_card(df, row_index):
    """Generate athlete card using native Streamlit components"""
    if row_index >= len(df):
        st.error("Athlete not found")
        return
        
    row = df.iloc[row_index]
    name_col, rank_col, score_col = get_column_names(df)
    
    # Check if we have the basic required columns
    if name_col is None or name_col not in df.columns:
        st.error("No athlete name column found in data")
        return
    
    # Get basic info
    name = safe_get_value(row, name_col)
    
    # Handle ranking display
    rank_display = "-"
    if rank_col and rank_col in df.columns:
        rank_val = row.get(rank_col, "")
        if not pd.isna(rank_val) and rank_val != '':
            try:
                rank_display = str(int(float(rank_val)))
            except (ValueError, TypeError):
                rank_display = str(rank_val)
    
    # Get status
    status = row.get("Status", "")
    styling = get_status_styling(status)
    
    # Create the card using a more minimal approach
    with st.container():
        # Header
        st.markdown(f"### #{rank_display} {name}")
        
        # Create columns for layout
        col1, col2 = st.columns(2)
        
        with col1:
            # Score information
            if score_col and score_col in df.columns:
                total_score = safe_get_value(row, score_col)
                if total_score != 'N/A':
                    st.write(f"**Total Score:** {total_score}")
            
            # Boulder scores if available
            boulder_scores = []
            for i in range(1, 5):
                col_name = f'Boulder {i} Score'
                if col_name in df.columns:
                    score = safe_get_value(row, col_name)
                    if score != 'N/A':
                        boulder_scores.append(score)
            
            if boulder_scores:
                st.write(f"**Boulder Scores:** {', '.join(boulder_scores)}")
        
        with col2:
            # Points information - check if columns exist first
            points_mapping = {
                'Points to 1st': 'Points for 1st Place',
                'Points to 2nd': 'Points for 2nd Place', 
                'Points to 3rd': 'Points for 3rd Place'
            }
            
            for primary, secondary in points_mapping.items():
                if primary in df.columns:
                    points = safe_get_value(row, primary)
                elif secondary in df.columns:
                    points = safe_get_value(row, secondary)
                else:
                    continue
                    
                if points != 'N/A':
                    label = primary.replace('Points for', 'Points for')
                    st.write(f"**{label}:** {points}")
            
            # Additional info - check if columns exist
            if 'Worst Finish' in df.columns:
                worst_finish = safe_get_value(row, 'Worst Finish')
                if worst_finish != 'N/A':
                    st.write(f"**Worst Finish:** {worst_finish}")
            elif 'Worst Possible Finish' in df.columns:
                worst_finish = safe_get_value(row, 'Worst Possible Finish')
                if worst_finish != 'N/A':
                    st.write(f"**Worst Possible Finish:** {worst_finish}")
            
            if 'Min to Qualify' in df.columns:
                min_to_qualify = safe_get_value(row, 'Min to Qualify')
                if min_to_qualify != 'N/A':
                    st.write(f"**Min to Qualify:** {min_to_qualify}")
            elif 'Points Needed for Top 8' in df.columns:
                min_to_qualify = safe_get_value(row, 'Points Needed for Top 8')
                if min_to_qualify != 'N/A':
                    st.write(f"**Points Needed for Top 8:** {min_to_qualify}")
        
        # Status badge
        st.write(f"**Status:** {styling['badge']}")
        
        # Add some spacing
        st.write("")

def display_competition_info():
    """Display competition qualification rules"""
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

def main():
    """Main application function"""
    setup_page()
    
    # Sidebar round selector
    with st.sidebar:
        selected_round = st.selectbox("Select Round", list(SHEETS_URLS.keys()))
    
    # Load and process data
    df = load_data(SHEETS_URLS[selected_round])
    
    if df is None or df.empty:
        st.error("No data loaded for this round.")
        st.stop()
    
    df = clean_data(df)
    name_col, rank_col, score_col = get_column_names(df)
    
    # Create and display leaderboard in sidebar
    leaderboard = create_leaderboard(df, name_col, rank_col, score_col)
    st.sidebar.table(leaderboard)
    
    # Main page content
    st.title("🏆 Seoul World Champs 2025")
    display_competition_info()
    
    # Athlete selector section
    st.title("👟 Athlete Rankings")
    
    # Create athlete selector (preserving original order)
    athletes_display = []
    if name_col in df.columns:
        for index, row in df.iterrows():
            name = row.get(name_col, '')
            if pd.notna(name) and str(name).strip() != "":
                rank_val = row.get(rank_col, "") if rank_col else ""
                rank_display = "-"
                if not pd.isna(rank_val) and rank_val != '':
                    try:
                        rank_display = str(int(float(rank_val)))
                    except (ValueError, TypeError):
                        rank_display = str(rank_val)
                athletes_display.append(f"{rank_display}. {name}")
        
        if athletes_display:
            selected_display = st.selectbox("Select an athlete", athletes_display)
            if selected_display:
                selected_name = selected_display.split(". ", 1)[1] if ". " in selected_display else selected_display
                original_athlete_row = df[df[name_col] == selected_name]
                
                if not original_athlete_row.empty:
                    original_index = original_athlete_row.index[0]
                    selected_row = original_athlete_row.iloc[0]
                    
                    if rank_col:
                        ranking = pd.to_numeric(selected_row[rank_col], errors='coerce')
                        if pd.notna(ranking):
                            st.subheader(f"{selected_row[name_col]} — #{int(ranking)}")
                        else:
                            st.subheader(f"{selected_row[name_col]}")
                    else:
                        st.subheader(f"{selected_row[name_col]}")
                    
                    generate_athlete_card(df, original_index)
    
    # All athletes section with expandable cards
    st.subheader("📋 All Athletes")
    
    df_sorted = df.copy()
    if rank_col in df_sorted.columns:
        df_sorted[rank_col] = pd.to_numeric(df_sorted[rank_col], errors='coerce')
        
        # Athletes with rankings (sorted)
        athletes_with_ranking = df_sorted[df_sorted[rank_col].notna()].sort_values(by=rank_col)
        for original_index, row in athletes_with_ranking.iterrows():
            name = row[name_col]
            ranking = int(row[rank_col])
            status = str(row.get("Status", "")).strip().lower()
            
            # Status emoji for expander
            if "qualified" in status and "eliminated" not in status:
                expander_label = f"🟢 #{ranking} - {name}"
            elif "eliminated" in status:
                expander_label = f"🔴 #{ranking} - {name}"
            elif "still in contention" in status:
                expander_label = f"🟡 #{ranking} - {name}"
            else:
                expander_label = f"#{ranking} - {name}"
            
            with st.expander(expander_label):
                generate_athlete_card(df, original_index)
        
        # Athletes without rankings
        athletes_without_ranking = df_sorted[df_sorted[rank_col].isna()]
        for original_index, row in athletes_without_ranking.iterrows():
            name = row[name_col]
            if pd.notna(name) and str(name).strip() != "":
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
                    generate_athlete_card(df, original_index)
    else:
        # No ranking column available
        for original_index, row in df_sorted.iterrows():
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
                    generate_athlete_card(df, original_index)
    
    st.write("Made by Elle ✨")

if __name__ == "__main__":
    main()
