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
    st.set_page_config(page_title="IFSC 2025 World Champs", layout="wide", initial_sidebar_state="expanded")
    
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
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(0, 0, 0, 0.1);
    }
    
    /* Filter section */
    .filter-section {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
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

def determine_boulder_status(row, rank_col):
    """Determine qualification status for boulder events"""
    if rank_col and rank_col in row:
        rank = row.get(rank_col, 999)
        try:
            rank = int(float(rank))
            if rank <= 8:  # Top 8 typically qualify for finals
                return "qualified"
            elif rank <= 20:  # Still possible depending on format
                return "still in contention"  
            else:
                return "eliminated"
        except (ValueError, TypeError):
            pass
    
    # Fallback - check if they have any performance data
    has_performance = False
    for i in range(1, 5):
        if f'B{i}T' in row or f'B{i}Z' in row:
            if row.get(f'B{i}T', 0) > 0 or row.get(f'B{i}Z', 0) > 0:
                has_performance = True
                break
    
    return "still in contention" if has_performance else "unknown"

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

def safe_get_value(row, column_name):
    """Safely get value from row, handling missing data"""
    val = row.get(column_name, '')
    return 'N/A' if pd.isna(val) or val == '' else str(val)

def create_compact_leaderboard(df, name_col, rank_col, score_col):
    """Create a more compact and visual leaderboard"""
    if df.empty or name_col is None:
        return "No data available"
    
    leaderboard_df = df.copy()
    
    if rank_col and rank_col in leaderboard_df.columns:
        leaderboard_df[rank_col] = pd.to_numeric(leaderboard_df[rank_col], errors='coerce')
        leaderboard_df = leaderboard_df.dropna(subset=[rank_col])
        
        if not leaderboard_df.empty:
            leaderboard_df = leaderboard_df.sort_values(by=rank_col)
            
            # Create HTML leaderboard
            html_content = '<div class="compact-leaderboard"><h4>🏆 Top 10 Leaderboard</h4>'
            
            for i, (_, row) in enumerate(leaderboard_df.head(10).iterrows()):
                rank = int(row[rank_col])
                name = row[name_col]
                
                # Determine status
                status = row.get("Status", "")
                if not status or pd.isna(status):
                    status = determine_boulder_status(row, rank_col)
                
                status_info = get_status_info(status)
                
                # Medal emojis for top 3
                medal = ""
                if rank == 1:
                    medal = "🥇"
                elif rank == 2:
                    medal = "🥈"
                elif rank == 3:
                    medal = "🥉"
                
                html_content += f'''
                <div style="display: flex; justify-content: space-between; align-items: center; 
                           padding: 8px; margin: 5px 0; background: rgba(0,0,0,0.1); 
                           border-radius: 8px;">
                    <span style="font-weight: bold;">{medal} #{rank} {name}</span>
                    <span>{status_info['emoji']}</span>
                </div>
                '''
            
            html_content += '</div>'
            return html_content
    
    return "No ranking data available"

def create_athlete_filters(df, name_col, rank_col):
    """Create filtering options for athletes"""
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.subheader("🔍 Filters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Status filter
        status_options = ["All", "Qualified", "Still in Contention", "Eliminated"]
        selected_status = st.selectbox("Status", status_options)
    
    with col2:
        # Ranking range filter
        if rank_col and rank_col in df.columns:
            max_rank = int(df[rank_col].max()) if df[rank_col].notna().any() else 50
            rank_range = st.slider("Rank Range", 1, max_rank, (1, max_rank))
        else:
            rank_range = None
    
    with col3:
        # Search by name
        search_term = st.text_input("Search Athlete", placeholder="Enter name...")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return selected_status, rank_range, search_term

def filter_athletes(df, name_col, rank_col, selected_status, rank_range, search_term):
    """Apply filters to the dataframe"""
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
            
            # Filter based on calculated or existing status
            mask = filtered_df.apply(lambda row: 
                target_status in str(row.get("Status", "")).lower() or
                target_status in determine_boulder_status(row, rank_col).lower(),
                axis=1
            )
            filtered_df = filtered_df[mask]
    
    return filtered_df

def create_athlete_card_html(row, name_col, rank_col, score_col, df_columns):
    """Create an HTML athlete card"""
    name = safe_get_value(row, name_col)
    
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
        status = determine_boulder_status(row, rank_col)
    
    status_info = get_status_info(status)
    
    # Boulder performance
    boulder_html = ""
    boulder_results = []
    for i in range(1, 5):
        top_col = f'B{i}T'
        zone_col = f'B{i}Z'
        att_col = f'B{i}Att'
        
        if all(col in df_columns for col in [top_col, zone_col, att_col]):
            top = int(row.get(top_col, 0)) if pd.notna(row.get(top_col)) else 0
            zone = int(row.get(zone_col, 0)) if pd.notna(row.get(zone_col)) else 0
            att = int(row.get(att_col, 0)) if pd.notna(row.get(att_col)) else 0
            
            if top > 0:
                result = f"<span style='color: #28a745; font-weight: bold;'>B{i}: {top}T{att}</span>"
            elif zone > 0:
                result = f"<span style='color: #ffc107; font-weight: bold;'>B{i}: {zone}Z{att}</span>"
            else:
                result = f"<span style='color: #6c757d;'>B{i}: -{att}</span>"
            boulder_results.append(result)
    
    if boulder_results:
        boulder_html = f"<div class='boulder-performance'><strong>Boulder Performance:</strong><br>{' | '.join(boulder_results)}</div>"
    
    # Score info
    score_html = ""
    if score_col and score_col in df_columns:
        total_score = safe_get_value(row, score_col)
        if total_score != 'N/A':
            score_html = f"<div><strong>Total Score:</strong> {total_score}</div>"
    
    # Ranking summary for boulder
    ranking_summary_html = ""
    if 'Ranking_Summary' in df_columns:
        ranking_summary = safe_get_value(row, 'Ranking_Summary')
        if ranking_summary != 'N/A':
            ranking_summary_html = f"<div><strong>Performance Summary:</strong> {ranking_summary}</div>"
    
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
    
    # Header
    st.markdown('''
    <div class="main-header">
        <h1 style="margin: 0; text-align: center;">🏔️ Seoul World Championships 2025</h1>
        <p style="margin: 5px 0 0 0; text-align: center; opacity: 0.8;">Live Competition Tracking</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Sidebar setup
    with st.sidebar:
        st.markdown("### 🎯 Competition Selection")
        selected_round = st.selectbox("Select Round", list(SHEETS_URLS.keys()), key="round_selector")
        
        # Auto-refresh toggle
        auto_refresh = st.checkbox("Auto-refresh (2s)", value=True)
        if auto_refresh:
            import time
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
    
    # Display leaderboard in sidebar
    with st.sidebar:
        leaderboard_html = create_compact_leaderboard(df, name_col, rank_col, score_col)
        st.markdown(leaderboard_html, unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Filters
        selected_status, rank_range, search_term = create_athlete_filters(df, name_col, rank_col)
        
        # Stats
        st.markdown("### 📊 Quick Stats")
        total_athletes = len(df)
        qualified_count = len(df[df.apply(lambda row: "qualified" in determine_boulder_status(row, rank_col).lower(), axis=1)])
        
        st.metric("Total Athletes", total_athletes)
        st.metric("Qualified", qualified_count)
        st.metric("Remaining", total_athletes - qualified_count)
    
    with col2:
        st.markdown(f"### 🏃‍♂️ {selected_round} - Athletes")
        
        # Apply filters
        filtered_df = filter_athletes(df, name_col, rank_col, selected_status, rank_range, search_term)
        
        if filtered_df.empty:
            st.warning("No athletes match the current filters.")
        else:
            # Sort for display
            if rank_col and rank_col in filtered_df.columns:
                filtered_df = filtered_df.sort_values(by=rank_col)
            
            # Display athlete cards in a more compact grid
            st.markdown(f"Showing {len(filtered_df)} athletes")
            
            # Create cards
            for idx, (_, row) in enumerate(filtered_df.iterrows()):
                if name_col and pd.notna(row.get(name_col)):
                    card_html = create_athlete_card_html(row, name_col, rank_col, score_col, filtered_df.columns)
                    st.markdown(card_html, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("Made by Elle ✨ | Data updates every 2 seconds")

if __name__ == "__main__":
    main()
