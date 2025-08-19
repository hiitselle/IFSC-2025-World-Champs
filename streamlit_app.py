import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

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
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="IFSC 2025 Seoul World Championships", 
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="🧗‍♀️"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f4e79;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
        border-bottom: 3px solid #e74c3c;
    }
    
    .round-header {
        background: linear-gradient(90deg, #3498db, #2ecc71);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .athlete-card {
        background: white;
        border: 2px solid #ecf0f1;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .athlete-card:hover {
        border-color: #3498db;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .rank-badge {
        background: #e74c3c;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-right: 1rem;
    }
    
    .gold { background: #f1c40f; color: #2c3e50; }
    .silver { background: #95a5a6; color: white; }
    .bronze { background: #e67e22; color: white; }
    
    .boulder-score {
        background: #f8f9fa;
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.2rem;
        display: inline-block;
        font-family: monospace;
        border-left: 4px solid #3498db;
    }
    
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .comparison-table {
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data(sheets_url):
    """Load data from Google Sheets with error handling"""
    try:
        df = pd.read_csv(sheets_url)
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_all_data():
    """Load all competition data"""
    all_data = {}
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, (round_name, url) in enumerate(SHEETS_URLS.items()):
        status_text.text(f"Loading {round_name}...")
        df = load_data(url)
        if not df.empty:
            all_data[round_name] = df
        progress_bar.progress((i + 1) / len(SHEETS_URLS))
    
    status_text.text("Data loading complete!")
    progress_bar.empty()
    status_text.empty()
    
    return all_data

def get_column_names(df):
    """Determine which column names to use based on available columns"""
    name_col = None
    possible_name_cols = ['Name', 'Athlete Name', 'name', 'athlete_name', 'Athlete', 'Climber']
    for col in possible_name_cols:
        if col in df.columns:
            name_col = col
            break
    
    if name_col is None:
        for col in df.columns:
            if 'name' in col.lower():
                name_col = col
                break
    
    rank_col = None
    possible_rank_cols = ['Live_Rank', 'Current Rank', 'Current Position', 'Rank', 'Position', 'rank', 'position']
    for col in possible_rank_cols:
        if col in df.columns:
            rank_col = col
            break
    
    score_col = None
    possible_score_cols = ['Manual Score', 'Total Score', 'Score', 'score', 'total_score']
    for col in possible_score_cols:
        if col in df.columns:
            score_col = col
            break
    
    return name_col, rank_col, score_col

def get_boulder_performance(row, boulder_num):
    """Extract boulder performance data"""
    top_col = f'B{boulder_num}T'
    zone_col = f'B{boulder_num}Z'
    att_col = f'B{boulder_num}Att'
    
    top = row.get(top_col, 0)
    zone = row.get(zone_col, 0)
    att = row.get(att_col, 0)
    
    return top, zone, att

def display_athlete_card(athlete_data, rank, name_col, score_col, round_name):
    """Display an enhanced athlete card"""
    name = athlete_data.get(name_col, "Unknown")
    score = athlete_data.get(score_col, "N/A") if score_col else "N/A"
    
    # Determine rank badge color
    badge_class = "rank-badge"
    if rank == 1:
        badge_class += " gold"
    elif rank == 2:
        badge_class += " silver"
    elif rank == 3:
        badge_class += " bronze"
    
    # Create the card HTML
    card_html = f"""
    <div class="athlete-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div>
                <span class="{badge_class}">#{rank}</span>
                <span style="font-size: 1.2rem; font-weight: bold; color: #2c3e50;">{name}</span>
            </div>
            <div style="font-size: 1.1rem; color: #7f8c8d;">
                Score: <strong>{score}</strong>
            </div>
        </div>
    """
    
    # Add boulder performance if it's a boulder round
    if "Boulder" in round_name:
        boulder_html = "<div style='margin-top: 1rem;'>"
        for i in range(1, 5):
            top, zone, att = get_boulder_performance(athlete_data, i)
            status = "🔴"  # Default red
            if top > 0:
                status = "🟢"  # Green for top
            elif zone > 0:
                status = "🟡"  # Yellow for zone
                
            boulder_html += f"""
            <span class="boulder-score">
                {status} B{i}: {top}T{zone}Z({att}att)
            </span>
            """
        boulder_html += "</div>"
        card_html += boulder_html
    
    # Add lead performance if it's a lead round
    elif "Lead" in round_name:
        height_col = None
        for col in athlete_data.index:
            if 'height' in col.lower() or 'hold' in col.lower():
                height_col = col
                break
        
        if height_col:
            height = athlete_data.get(height_col, "N/A")
            card_html += f"""
            <div style='margin-top: 1rem;'>
                <span class="boulder-score">
                    📏 Height: {height}
                </span>
            </div>
            """
    
    card_html += "</div>"
    
    st.markdown(card_html, unsafe_allow_html=True)

def create_athlete_comparison_chart(all_data, selected_athletes):
    """Create a comparison chart for selected athletes across rounds"""
    if not selected_athletes:
        return None
    
    comparison_data = []
    
    for athlete_name in selected_athletes:
        athlete_rounds = {}
        
        for round_name, df in all_data.items():
            name_col, rank_col, score_col = get_column_names(df)
            if name_col:
                athlete_row = df[df[name_col].str.contains(athlete_name, case=False, na=False)]
                if not athlete_row.empty:
                    rank = athlete_row.iloc[0].get(rank_col, None) if rank_col else None
                    score = athlete_row.iloc[0].get(score_col, None) if score_col else None
                    
                    if rank is not None and str(rank).isdigit():
                        athlete_rounds[round_name] = int(rank)
        
        for round_name, rank in athlete_rounds.items():
            comparison_data.append({
                'Athlete': athlete_name,
                'Round': round_name,
                'Rank': rank
            })
    
    if comparison_data:
        comparison_df = pd.DataFrame(comparison_data)
        
        fig = px.line(comparison_df, 
                     x='Round', 
                     y='Rank', 
                     color='Athlete',
                     title='Athlete Performance Comparison Across Rounds',
                     markers=True)
        
        # Invert y-axis so rank 1 is at the top
        fig.update_layout(yaxis=dict(autorange='reversed'))
        fig.update_traces(line=dict(width=3), marker=dict(size=8))
        
        return fig
    
    return None

def athlete_detail_view(all_data, athlete_name):
    """Show detailed view for a specific athlete"""
    st.markdown(f"""
    <div class="round-header">
        🏆 Detailed Performance: {athlete_name}
    </div>
    """, unsafe_allow_html=True)
    
    athlete_data = {}
    
    for round_name, df in all_data.items():
        name_col, rank_col, score_col = get_column_names(df)
        if name_col:
            athlete_row = df[df[name_col].str.contains(athlete_name, case=False, na=False)]
            if not athlete_row.empty:
                athlete_data[round_name] = athlete_row.iloc[0]
    
    if not athlete_data:
        st.warning(f"No data found for athlete: {athlete_name}")
        return
    
    # Create columns for different rounds
    cols = st.columns(min(len(athlete_data), 4))
    
    for i, (round_name, data) in enumerate(athlete_data.items()):
        with cols[i % 4]:
            st.markdown(f"**{round_name}**")
            name_col, rank_col, score_col = get_column_names(pd.DataFrame([data]))
            rank = data.get(rank_col, "N/A") if rank_col else "N/A"
            score = data.get(score_col, "N/A") if score_col else "N/A"
            
            st.metric("Rank", rank)
            st.metric("Score", score)
            
            # Show boulder performance
            if "Boulder" in round_name:
                st.markdown("**Boulder Performance:**")
                for b in range(1, 5):
                    top, zone, att = get_boulder_performance(data, b)
                    status = "🟢" if top > 0 else "🟡" if zone > 0 else "🔴"
                    st.write(f"{status} B{b}: {top}T{zone}Z({att}att)")

def main():
    """Main application function"""
    setup_page()
    
    # Header
    st.markdown("""
    <div class="main-header">
        🧗‍♀️ IFSC 2025 Seoul World Championships
    </div>
    """, unsafe_allow_html=True)
    
    # Load all data
    with st.spinner("Loading competition data..."):
        all_data = load_all_data()
    
    if not all_data:
        st.error("No data could be loaded. Please check your internet connection.")
        return
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 🎯 Navigation")
        
        app_mode = st.selectbox(
            "Choose view:",
            ["Competition Results", "Athlete Comparison", "Athlete Detail", "Statistics", "Debug Mode"]
        )
        
        if app_mode in ["Competition Results", "Debug Mode"]:
            selected_round = st.selectbox("Select Round:", list(all_data.keys()))
        
        if app_mode == "Athlete Comparison":
            # Get all unique athlete names
            all_athletes = set()
            for df in all_data.values():
                name_col, _, _ = get_column_names(df)
                if name_col and name_col in df.columns:
                    all_athletes.update(df[name_col].dropna().tolist())
            
            selected_athletes = st.multiselect(
                "Select athletes to compare:",
                sorted(list(all_athletes)),
                max_selections=5
            )
        
        if app_mode == "Athlete Detail":
            # Get all unique athlete names
            all_athletes = set()
            for df in all_data.values():
                name_col, _, _ = get_column_names(df)
                if name_col and name_col in df.columns:
                    all_athletes.update(df[name_col].dropna().tolist())
            
            selected_athlete = st.selectbox(
                "Select athlete:",
                [""] + sorted(list(all_athletes))
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick stats
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 📊 Quick Stats")
        total_athletes = sum(len(df) for df in all_data.values())
        st.metric("Total Entries", total_athletes)
        st.metric("Rounds", len(all_data))
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content
    if app_mode == "Competition Results":
        df = all_data.get(selected_round, pd.DataFrame())
        
        if df.empty:
            st.error(f"No data available for {selected_round}")
            return
        
        # Round header
        st.markdown(f"""
        <div class="round-header">
            🏆 {selected_round}
        </div>
        """, unsafe_allow_html=True)
        
        # Display athletes
        name_col, rank_col, score_col = get_column_names(df)
        
        if name_col is None:
            st.error("Could not find athlete names in the data")
            return
        
        # Sort by rank if available
        if rank_col and rank_col in df.columns:
            df_sorted = df.sort_values(by=rank_col, na_position='last')
        else:
            df_sorted = df
        
        # Display in columns
        cols = st.columns(2)
        for idx, (_, athlete_data) in enumerate(df_sorted.iterrows()):
            rank = athlete_data.get(rank_col, idx + 1) if rank_col else idx + 1
            
            with cols[idx % 2]:
                display_athlete_card(athlete_data, rank, name_col, score_col, selected_round)
    
    elif app_mode == "Athlete Comparison":
        if selected_athletes:
            # Create comparison chart
            fig = create_athlete_comparison_chart(all_data, selected_athletes)
            
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Show detailed comparison table
            st.markdown("### 📋 Detailed Comparison")
            
            comparison_table = []
            for athlete_name in selected_athletes:
                row_data = {"Athlete": athlete_name}
                
                for round_name, df in all_data.items():
                    name_col, rank_col, score_col = get_column_names(df)
                    if name_col:
                        athlete_row = df[df[name_col].str.contains(athlete_name, case=False, na=False)]
                        if not athlete_row.empty:
                            rank = athlete_row.iloc[0].get(rank_col, "N/A") if rank_col else "N/A"
                            row_data[round_name] = rank
                        else:
                            row_data[round_name] = "N/A"
                
                comparison_table.append(row_data)
            
            if comparison_table:
                comparison_df = pd.DataFrame(comparison_table)
                st.dataframe(comparison_df, use_container_width=True)
        else:
            st.info("Please select athletes to compare using the sidebar.")
    
    elif app_mode == "Athlete Detail":
        if selected_athlete:
            athlete_detail_view(all_data, selected_athlete)
        else:
            st.info("Please select an athlete using the sidebar.")
    
    elif app_mode == "Statistics":
        st.markdown("""
        <div class="round-header">
            📈 Competition Statistics
        </div>
        """, unsafe_allow_html=True)
        
        # Create statistics visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Participation by round
            participation_data = []
            for round_name, df in all_data.items():
                participation_data.append({
                    "Round": round_name,
                    "Athletes": len(df),
                    "Gender": "Male" if "Male" in round_name else "Female",
                    "Discipline": "Boulder" if "Boulder" in round_name else "Lead"
                })
            
            participation_df = pd.DataFrame(participation_data)
            
            fig1 = px.bar(participation_df, 
                         x="Round", 
                         y="Athletes",
                         color="Gender",
                         title="Participation by Round")
            fig1.update_xaxis(tickangle=45)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Discipline distribution
            fig2 = px.pie(participation_df, 
                         values="Athletes", 
                         names="Discipline",
                         title="Athletes by Discipline")
            st.plotly_chart(fig2, use_container_width=True)
    
    elif app_mode == "Debug Mode":
        df = all_data.get(selected_round, pd.DataFrame())
        
        st.markdown(f"""
        <div class="round-header">
            🔧 Debug Mode: {selected_round}
        </div>
        """, unsafe_allow_html=True)
        
        if df.empty:
            st.error(f"No data available for {selected_round}")
            return
        
        # Debug information
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 DataFrame Info")
            st.write(f"**Shape:** {df.shape}")
            st.write(f"**Columns:** {len(df.columns)}")
            st.write(f"**Rows:** {len(df)}")
            
            st.subheader("📋 Columns")
            for i, col in enumerate(df.columns):
                st.write(f"{i+1}. `{col}` ({df[col].dtype})")
        
        with col2:
            st.subheader("🎯 Column Detection")
            name_col, rank_col, score_col = get_column_names(df)
            
            st.write(f"**Name Column:** `{name_col}`")
            st.write(f"**Rank Column:** `{rank_col}`")
            st.write(f"**Score Column:** `{score_col}`")
            
            # Show sample data
            st.subheader("🔍 Sample Data")
            st.dataframe(df.head(3))

if __name__ == "__main__":
    main()
