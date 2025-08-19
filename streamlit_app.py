import streamlit as st
import pandas as pd
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

def setup_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="IFSC 2025 World Champs - Debug", 
        layout="wide"
    )

@st.cache_data(ttl=60)  # Cache for 60 seconds for debugging
def load_data(sheets_url):
    """Load data from Google Sheets with detailed error reporting"""
    try:
        st.write(f"🔄 Attempting to load data from: {sheets_url}")
        df = pd.read_csv(sheets_url)
        st.success(f"✅ Data loaded successfully! Shape: {df.shape}")
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.write(f"Error type: {type(e).__name__}")
        return pd.DataFrame()

def debug_dataframe(df, round_name):
    """Debug function to inspect the dataframe"""
    st.subheader(f"🔍 Debug Information for {round_name}")
    
    if df.empty:
        st.error("❌ DataFrame is empty!")
        return
    
    # Basic info
    st.write(f"**DataFrame Shape:** {df.shape}")
    st.write(f"**Number of rows:** {len(df)}")
    st.write(f"**Number of columns:** {len(df.columns)}")
    
    # Column names
    st.subheader("📋 Available Columns:")
    for i, col in enumerate(df.columns):
        st.write(f"{i+1}. `{col}` (dtype: {df[col].dtype})")
    
    # Show first few rows
    st.subheader("📊 First 5 Rows:")
    st.dataframe(df.head())
    
    # Check for common name columns
    st.subheader("🔍 Column Detection:")
    name_candidates = []
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in ['name', 'athlete', 'climber', 'competitor']):
            name_candidates.append(col)
    
    if name_candidates:
        st.success(f"✅ Found potential name columns: {name_candidates}")
    else:
        st.warning("⚠️ No obvious name columns found")
    
    # Check for rank columns
    rank_candidates = []
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in ['rank', 'position', 'place']):
            rank_candidates.append(col)
    
    if rank_candidates:
        st.success(f"✅ Found potential rank columns: {rank_candidates}")
    else:
        st.warning("⚠️ No obvious rank columns found")
    
    # Check for boulder columns
    boulder_candidates = []
    for col in df.columns:
        if col.startswith('B') and any(col.endswith(suffix) for suffix in ['T', 'Z', 'Att']):
            boulder_candidates.append(col)
    
    if boulder_candidates:
        st.success(f"✅ Found boulder columns: {boulder_candidates}")
    else:
        st.warning("⚠️ No boulder performance columns found")
    
    # Show non-null counts
    st.subheader("📈 Data Completeness:")
    non_null_counts = df.count()
    for col in df.columns:
        percentage = (non_null_counts[col] / len(df)) * 100
        st.write(f"**{col}**: {non_null_counts[col]}/{len(df)} ({percentage:.1f}% complete)")

def get_column_names(df):
    """Determine which column names to use based on available columns"""
    # Name column
    name_col = None
    possible_name_cols = ['Name', 'Athlete Name', 'name', 'athlete_name', 'Athlete', 'Climber']
    for col in possible_name_cols:
        if col in df.columns:
            name_col = col
            break
    
    # If no exact match, look for columns containing 'name'
    if name_col is None:
        for col in df.columns:
            if 'name' in col.lower():
                name_col = col
                break
    
    # Rank column
    rank_col = None
    possible_rank_cols = ['Live_Rank', 'Current Rank', 'Current Position', 'Rank', 'Position', 'rank', 'position']
    for col in possible_rank_cols:
        if col in df.columns:
            rank_col = col
            break
    
    # Score column
    score_col = None
    possible_score_cols = ['Manual Score', 'Total Score', 'Score', 'score', 'total_score']
    for col in possible_score_cols:
        if col in df.columns:
            score_col = col
            break
    
    return name_col, rank_col, score_col

def simple_athlete_display(df, name_col, rank_col, score_col):
    """Simple display of athletes for debugging"""
    if df.empty:
        st.warning("No data to display")
        return
    
    st.subheader("👥 Athletes Found:")
    
    if name_col is None:
        st.error("❌ Could not find a name column")
        st.write("Available columns:", list(df.columns))
        return
    
    # Display athletes in a simple format
    for idx, (_, row) in enumerate(df.iterrows()):
        name = row.get(name_col, "Unknown")
        rank = row.get(rank_col, "N/A") if rank_col else "N/A"
        score = row.get(score_col, "N/A") if score_col else "N/A"
        
        st.write(f"**{idx+1}. {name}** - Rank: {rank} - Score: {score}")
        
        # Show boulder data if available
        boulder_info = []
        for i in range(1, 5):
            top_col = f'B{i}T'
            zone_col = f'B{i}Z'
            att_col = f'B{i}Att'
            
            if all(col in df.columns for col in [top_col, zone_col, att_col]):
                top = row.get(top_col, 0)
                zone = row.get(zone_col, 0)
                att = row.get(att_col, 0)
                boulder_info.append(f"B{i}: {top}T{zone}Z({att}att)")
        
        if boulder_info:
            st.write(f"   └─ {' | '.join(boulder_info)}")
        
        if idx >= 9:  # Show first 10 for debugging
            st.write(f"... and {len(df) - 10} more athletes")
            break

def main():
    """Main debugging function"""
    setup_page()
    
    st.title("🔧 Seoul World Championships 2025 - Debug Mode")
    st.write("This debug version will help identify why athlete data isn't showing.")
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Select Competition")
        selected_round = st.selectbox("Round", list(SHEETS_URLS.keys()))
        
        st.header("⚙️ Debug Options")
        show_raw_data = st.checkbox("Show raw DataFrame", False)
        show_debug_info = st.checkbox("Show debug information", True)
    
    # Load data
    st.header(f"📊 Loading: {selected_round}")
    df = load_data(SHEETS_URLS[selected_round])
    
    # Show raw data if requested
    if show_raw_data and not df.empty:
        st.subheader("📋 Raw Data")
        st.dataframe(df)
    
    # Debug information
    if show_debug_info:
        debug_dataframe(df, selected_round)
    
    # Try to identify columns and show athletes
    if not df.empty:
        name_col, rank_col, score_col = get_column_names(df)
        
        st.subheader("🎯 Column Mapping Results:")
        st.write(f"**Name Column:** {name_col}")
        st.write(f"**Rank Column:** {rank_col}")
        st.write(f"**Score Column:** {score_col}")
        
        # Simple athlete display
        simple_athlete_display(df, name_col, rank_col, score_col)
    
    # Manual column selection for testing
    if not df.empty:
        st.subheader("🔧 Manual Column Selection")
        st.write("If the automatic detection failed, manually select columns:")
        
        manual_name_col = st.selectbox("Name Column", ["None"] + list(df.columns))
        manual_rank_col = st.selectbox("Rank Column", ["None"] + list(df.columns))
        
        if manual_name_col != "None":
            st.subheader("Manual Test Results:")
            for idx, (_, row) in enumerate(df.head(5).iterrows()):
                name = row.get(manual_name_col, "Unknown")
                rank = row.get(manual_rank_col, "N/A") if manual_rank_col != "None" else "N/A"
                st.write(f"{idx+1}. **{name}** (Rank: {rank})")

if __name__ == "__main__":
    main()
