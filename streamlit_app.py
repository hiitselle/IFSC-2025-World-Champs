import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time
from datetime import datetime

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

# Competition progress tracking
QUALIFICATION_RULES = {
    "Boulder Semis": {"qualify_count": 8, "total_problems": 4},
    "Boulder Final": {"qualify_count": 3, "total_problems": 4},
    "Lead Semis": {"qualify_count": 8, "total_problems": 1},
    "Lead Final": {"qualify_count": 3, "total_problems": 1}
}

def setup_page():
    """Configure Streamlit page settings and styling"""
    st.set_page_config(
        page_title="IFSC 2025 World Champs", 
        layout="wide", 
        initial_sidebar_state="expanded",
        page_icon="🧗"
    )
    
    # Enhanced styling with better colors and spacing
    st.markdown("""
    <style>
    /* Main background and text */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    
    /* Header styling */
    .main-header {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
    }
    
    .live-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #ff4444;
        border-radius: 50%;
        animation: pulse 2s infinite;
        margin-right: 8px;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Card styling */
    .athlete-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        color: #333;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.2s ease-in-out;
    }
    
    .athlete-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Status badges */
    .status-qualified {
        background: #d4edda;
        color: #155724;
        padding: 5px 12px;
        border-radius: 20px;
        border: 2px solid #28a745;
        font-weight: bold;
        display: inline-block;
        margin: 5px 0;
    }
    
    .status-eliminated {
        background: #f8d7da;
        color: #721c24;
        padding: 5px 12px;
        border-radius: 20px;
        border: 2px solid #dc3545;
        font-weight: bold;
        display: inline-block;
        margin: 5px 0;
    }
    
    .status-contention {
        background: #fff3cd;
        color: #856404;
        padding: 5px 12px;
        border-radius: 20px;
        border: 2px solid #ffc107;
        font-weight: bold;
        display: inline-block;
        margin: 5px 0;
    }
    
    /* Progress indicators */
    .progress-bar {
        background: #e9ecef;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #28a745, #20c997);
        transition: width 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 12px;
    }
    
    /* Compact leaderboard */
    .compact-leaderboard {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: #333;
    }
    
    /* Boulder performance styling */
    .boulder-performance {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        border-left: 4px solid #007bff;
        font-size: 14px;
    }
    
    .boulder-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin: 10px 0;
    }
    
    .boulder-problem {
        text-align: center;
        padding: 8px;
        border-radius: 8px;
        font-weight: bold;
    }
    
    .boulder-top {
        background: #d4edda;
        color: #155724;
        border: 2px solid #28a745;
    }
    
    .boulder-zone {
        background: #fff3cd;
        color: #856404;
        border: 2px solid #ffc107;
    }
    
    .boulder-none {
        background: #f8d7da;
        color: #721c24;
        border: 2px solid #dc3545;
    }
    
    /* Competition stats */
    .competition-stats {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Filter section */
    .filter-section {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Hide Streamlit elements */
    header[data-testid="stHeader"] {
        display: none;
    }
    
    .stDeployButton {
        display: none;
    }
    
    #MainMenu {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=2)  # Refresh every 2 seconds
def load_data(sheets_url):
    """Load data from Google Sheets with caching"""
    try:
        return pd.read_csv(sheets_url)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def clean_data(df):
    """Clean and standardize dataframe columns"""
    if df.empty:
        return df
        
    # Clean points columns
    points_columns = [
        'Points to 1st', 'Points to 2nd', 'Points to 3rd',
        'Points for 1st Place', 'Points for 2nd Place', 'Points for 3rd Place'
    ]
    
    for col in points_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna('')
    
    # Clean boulder-specific columns
    for i in range(1, 5):
        for suffix in ['T', 'Z', 'Att']:  # Top, Zone, Attempts
            col_name = f'B{i}{suffix}'
            if col_name in df.columns:
                df[col_name] = pd.to_numeric(df[col_name], errors='coerce').fillna(0)
    
    return df

def calculate_boulder_ranking(df):
    """Calculate live boulder ranking based on tops, zones, and attempts"""
    if df.empty:
        return df
    
    # Check if we have boulder data columns
    boulder_cols_exist = any(col.startswith('B') and col.endswith(('T', 'Z', 'Att')) for col in df.columns)
    if not boulder_cols_exist:
        return df
    
    df_ranked = df.copy()
    
    # Initialize totals
    df_ranked['Total_Tops'] = 0
    df_ranked['Total_Zones'] = 0  
    df_ranked['Total_Attempts'] = 0
    df_ranked['Top_Attempts'] = 0
    df_ranked['Zone_Attempts'] = 0
    
    # Sum across all 4 boulders
    for i in range(1, 5):
        top_col = f'B{i}T'
        zone_col = f'B{i}Z'  
        att_col = f'B{i}Att'
        
        if top_col in df.columns:
            df_ranked['Total_Tops'] += df_ranked[top_col].fillna(0)
        if zone_col in df.columns:
            df_ranked['Total_Zones'] += df_ranked[zone_col].fillna(0)
        if att_col in df.columns:
            df_ranked['Total_Attempts'] += df_ranked[att_col].fillna(0)
            
        # Calculate attempts to achieve tops and zones
        if top_col in df.columns and att_col in df.columns:
            top_attempts = df_ranked.apply(lambda row: row[att_col] if row[top_col] > 0 else 0, axis=1)
            df_ranked['Top_Attempts'] += top_attempts.fillna(0)
            
        if zone_col in df.columns and att_col in df.columns and top_col in df.columns:
            zone_attempts = df_ranked.apply(lambda row: row[att_col] if (row[zone_col] > 0 and row[top_col] == 0) else 0, axis=1)
            df_ranked['Zone_Attempts'] += zone_attempts.fillna(0)
    
    # Sort by boulder ranking criteria
    df_ranked = df_ranked.sort_values([
        'Total_Tops', 'Total_Zones', 'Top_Attempts', 'Zone_Attempts', 'Total_Attempts'
    ], ascending=[False, False, True, True, True])
    
    # Assign rankings
    df_ranked['Live_Rank'] = range(1, len(df_ranked) + 1)
    
    # Create a ranking summary
    df_ranked['Ranking_Summary'] = df_ranked.apply(lambda row: 
        f"{int(row['Total_Tops'])}T{int(row['Total_Zones'])}Z {int(row['Top_Attempts'])}/{int(row['Zone_Attempts'])}", axis=1)
    
    return df_ranked

def get_column_names(df):
    """Determine which column names to use based on available columns"""
    # Name column
    name_col = None
    for col in ['Name', 'Athlete Name', 'name', 'athlete_name']:
        if col in df.columns:
            name_col = col
            break
    
    # Rank column - prefer live calculated rank for boulder
    rank_col = None
    if 'Live_Rank' in df.columns:
        rank_col = 'Live_Rank'
    else:
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

def determine_qualification_status(row, rank_col, round_name):
    """Determine qualification status based on round and ranking"""
    if rank_col and rank_col in row:
        rank = row.get(rank_col, 999)
        try:
            rank = int(float(rank))
            
            # Determine qualification threshold based on round
            if "Semis" in round_name:
                qualify_threshold = 8
            elif "Final" in round_name:
                qualify_threshold = 3
            else:
                qualify_threshold = 8
            
            if rank <= qualify_threshold:
                return "qualified"
            elif rank <= qualify_threshold * 2:  # Still possible depending on format
                return "still in contention"  
            else:
                return "eliminated"
        except (ValueError, TypeError):
            pass
    
    return "unknown"

def get_status_info(status):
    """Return status information with emoji and styling"""
    status = str(status).strip().lower()
    
    if "qualified" in status and "eliminated" not in status:
        return {
            'emoji': '🟢',
            'text': 'Qualified',
            'class': 'status-qualified'
        }
    elif "eliminated" in status:
        return {
            'emoji': '🔴',
            'text': 'Eliminated',
            'class': 'status-eliminated'
        }
    elif "still in contention" in status:
        return {
            'emoji': '🟡',
            'text': 'Still in Contention',
            'class': 'status-contention'
        }
    else:
        return {
            'emoji': '⚪',
            'text': status.title() if status else 'Unknown',
            'class': 'status-unknown'
        }

def create_boulder_visualization(row):
    """Create visual representation of boulder performance"""
    boulder_html = '<div class="boulder-grid">'
    
    for i in range(1, 5):
        top_col = f'B{i}T'
        zone_col = f'B{i}Z'
        att_col = f'B{i}Att'
        
        top = int(row.get(top_col, 0)) if pd.notna(row.get(top_col)) else 0
        zone = int(row.get(zone_col, 0)) if pd.notna(row.get(zone_col)) else 0
        att = int(row.get(att_col, 0)) if pd.notna(row.get(att_col)) else 0
        
        if top > 0:
            boulder_html += f'<div class="boulder-problem boulder-top">B{i}<br>TOP<br>{att} att</div>'
        elif zone > 0:
            boulder_html += f'<div class="boulder-problem boulder-zone">B{i}<br>ZONE<br>{att} att</div>'
        else:
            boulder_html += f'<div class="boulder-problem boulder-none">B{i}<br>-<br>{att} att</div>'
    
    boulder_html += '</div>'
    return boulder_html

def create_competition_progress(df, round_name):
    """Create a progress indicator for the competition"""
    total_athletes = len(df)
    
    # Count athletes with any performance
    athletes_started = 0
    athletes_finished = 0
    
    if "Boulder" in round_name:
        for _, row in df.iterrows():
            has_started = False
            problems_completed = 0
            
            for i in range(1, 5):
                att_col = f'B{i}Att'
                if att_col in df.columns and pd.notna(row.get(att_col)) and row.get(att_col, 0) > 0:
                    has_started = True
                    problems_completed += 1
            
            if has_started:
                athletes_started += 1
                if problems_completed >= 4:  # Assuming 4 boulders
                    athletes_finished += 1
    
    progress_html = f'''
    <div class="competition-stats">
        <h4>🏁 Competition Progress</h4>
        <div style="display: flex; justify-content: space-between; margin: 10px 0;">
            <span>Started: {athletes_started}/{total_athletes}</span>
            <span>Finished: {athletes_finished}/{total_athletes}</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {(athletes_finished/total_athletes*100) if total_athletes > 0 else 0:.1f}%">
                {(athletes_finished/total_athletes*100) if total_athletes > 0 else 0:.1f}%
            </div>
        </div>
    </div>
    '''
    return progress_html

def create_enhanced_athlete_card(row, name_col, rank_col, score_col, df_columns, round_name):
    """Create an enhanced HTML athlete card with better visualizations"""
    name = row.get(name_col, "Unknown")
    
    # Handle ranking
    rank_display = "Unranked"
    if rank_col and rank_col in df_columns:
        rank_val = row.get(rank_col, "")
        if not pd.isna(rank_val) and rank_val != '':
            try:
                rank_display = f"#{int(float(rank_val))}"
            except (ValueError, TypeError):
                rank_display = f"#{str(rank_val)}"
    
    # Get status
    status = row.get("Status", "")
    if not status or pd.isna(status):
        status = determine_qualification_status(row, rank_col, round_name)
    
    status_info = get_status_info(status)
    
    # Boulder performance visualization
    boulder_html = ""
    if "Boulder" in round_name:
        boulder_html = f'<div style="margin: 15px 0;"><strong>Boulder Performance:</strong>{create_boulder_visualization(row)}</div>'
    
    # Score info
    score_html = ""
    if score_col and score_col in df_columns:
        total_score = row.get(score_col, 'N/A')
        if not pd.isna(total_score) and total_score != '':
            score_html = f"<div><strong>Score:</strong> {total_score}</div>"
    
    # Ranking summary
    ranking_summary_html = ""
    if 'Ranking_Summary' in df_columns:
        ranking_summary = row.get('Ranking_Summary', '')
        if not pd.isna(ranking_summary) and ranking_summary != '':
            ranking_summary_html = f"<div style='font-size: 14px; color: #666; margin: 5px 0;'><strong>Summary:</strong> {ranking_summary}</div>"
    
    card_html = f'''
    <div class="athlete-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h3 style="margin: 0; color: #333;">{rank_display} {name}</h3>
            <div class="{status_info['class']}">{status_info['emoji']} {status_info['text']}</div>
        </div>
        {score_html}
        {ranking_summary_html}
        {boulder_html}
    </div>
    '''
    
    return card_html

def main():
    """Main application function"""
    setup_page()
    
    # Initialize session state for auto-refresh
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
    
    # Header with live indicator
    current_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(f'''
    <div class="main-header">
        <h1 style="margin: 0;">🧗‍♂️ Seoul World Championships 2025</h1>
        <p style="margin: 5px 0 0 0; opacity: 0.8;">
            <span class="live-indicator"></span>Live Competition Tracking | Last updated: {current_time}
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Sidebar setup
    with st.sidebar:
        st.markdown("### 🎯 Competition Selection")
        selected_round = st.selectbox("Select Round", list(SHEETS_URLS.keys()), key="round_selector")
        
        # Auto-refresh settings
        st.markdown("### ⚙️ Settings")
        auto_refresh = st.checkbox("Auto-refresh (2s)", value=True)
        show_progress = st.checkbox("Show competition progress", value=True)
        
        if auto_refresh:
            time.sleep(2)
            st.rerun()
    
    # Load and process data
    with st.spinner("Loading competition data..."):
        df = load_data(SHEETS_URLS[selected_round])
    
    if df is None or df.empty:
        st.error("❌ No data loaded for this round.")
        st.stop()
    
    df = clean_data(df)
    
    # Calculate boulder rankings if this is a boulder event
    if "Boulder" in selected_round:
        df = calculate_boulder_ranking(df)
    
    name_col, rank_col, score_col = get_column_names(df)
    
    # Display competition progress
    with st.sidebar:
        if show_progress:
            progress_html = create_competition_progress(df, selected_round)
            st.markdown(progress_html, unsafe_allow_html=True)
        
        # Quick stats
        st.markdown("### 📊 Quick Stats")
        total_athletes = len(df)
        if rank_col:
            qualified_count = len(df[df.apply(lambda row: "qualified" in determine_qualification_status(row, rank_col, selected_round).lower(), axis=1)])
        else:
            qualified_count = 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total", total_athletes)
        with col2:
            st.metric("Qualified", qualified_count)
    
    # Main content layout
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Enhanced filters
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.subheader("🔍 Filters")
        
        # Status filter
        status_options = ["All", "Qualified", "Still in Contention", "Eliminated"]
        selected_status = st.selectbox("Status", status_options)
        
        # Ranking range filter
        if rank_col and rank_col in df.columns:
            max_rank = int(df[rank_col].max()) if df[rank_col].notna().any() else 50
            rank_range = st.slider("Rank Range", 1, max_rank, (1, min(20, max_rank)))
        else:
            rank_range = None
        
        # Search by name
        search_term = st.text_input("Search Athlete", placeholder="Enter name...")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"### 🏃‍♂️ {selected_round}")
        
        # Apply filters
        filtered_df = df.copy()
        
        # Apply name search
        if search_term and name_col:
            filtered_df = filtered_df[filtered_df[name_col].str.contains(search_term, case=False, na=False)]
        
        # Apply rank range filter
        if rank_range and rank_col and rank_col in filtered_df.columns:
            filtered_df = filtered_df[
                (filtered_df[rank_col] >= rank_range[0]) & 
                (filtered_df[rank_col] <= rank_range[1])
            ]
        
        # Apply status filter
        if selected_status != "All":
            status_mapping = {
                "Qualified": "qualified",
                "Still in Contention": "still in contention", 
                "Eliminated": "eliminated"
            }
            
            if selected_status in status_mapping:
                target_status = status_mapping[selected_status]
                mask = filtered_df.apply(lambda row: 
                    target_status in determine_qualification_status(row, rank_col, selected_round).lower(),
                    axis=1
                )
                filtered_df = filtered_df[mask]
        
        if filtered_df.empty:
            st.warning("No athletes match the current filters.")
        else:
            # Sort for display
            if rank_col and rank_col in filtered_df.columns:
                filtered_df = filtered_df.sort_values(by=rank_col)
            
            st.markdown(f"Showing **{len(filtered_df)}** of **{len(df)}** athletes")
            
            # Display enhanced athlete cards
            for idx, (_, row) in enumerate(filtered_df.iterrows()):
                if name_col and pd.notna(row.get(name_col)):
                    card_html = create_enhanced_athlete_card(
                        row, name_col, rank_col, score_col, filtered_df.columns, selected_round
                    )
                    st.markdown(card_html, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(f"Made with ❤️ by Elle ✨ | Updated every 2 seconds | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
