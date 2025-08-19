def display_athlete_card(athlete_data, rank, cols_mapping, round_name):
    """Display an enhanced athlete card using Streamlit components only"""
    name = athlete_data.get(cols_mapping.get('name', 'Name'), "Unknown")
    score = athlete_data.get(cols_mapping.get('score', 'Total Score'), "N/A")
    
    # Handle rank display
    if pd.isna(rank) or rank == "":
        rank_display = "N/A"
    else:
        try:
            rank_display = int(float(rank))
        except:
            rank_display = str(rank)
    
    # Get qualification status
    qual_status, qual_color = get_qualification_status(athlete_data, cols_mapping)
    
    # Use Streamlit container WITHOUT border parameter
    with st.container():
        # Create custom border using CSS
        st.markdown("""
        <div style="
            border: 2px solid #ecf0f1;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            background: white;
            position: relative;
        ">
        """, unsafe_allow_html=True)
        
        # Header row with rank and name
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Determine medal emoji
            if rank_display == 1:
                medal = "🥇"
            elif rank_display == 2:
                medal = "🥈"
            elif rank_display == 3:
                medal = "🥉"
            else:
                medal = "🏃"
            
            st.markdown(f"### {medal} #{rank_display} - {name}")
            
            if qual_status:
                if "Qualified" in qual_status:
                    st.success(qual_status)
                else:
                    st.error(qual_status)
        
        with col2:
            st.metric("Score", score)
        
        # Position information
        current_pos = athlete_data.get(cols_mapping.get('rank', 'Current Rank'), "N/A")
        worst_case = athlete_data.get(cols_mapping.get('worst_case', 'Worst Case Finish'), "N/A")
        
        pos_col1, pos_col2 = st.columns(2)
        with pos_col1:
            st.info(f"📍 Current: #{current_pos}")
        
        if pd.notna(worst_case) and str(worst_case) != "N/A":
            with pos_col2:
                st.warning(f"⚠️ Worst: #{worst_case}")
        
        # Add performance data based on round type
        if "Boulder" in round_name:
            display_boulder_performance(athlete_data, cols_mapping)
        elif "Lead" in round_name:
            display_lead_performance(athlete_data, cols_mapping)
        
        # Close the custom border div
        st.markdown("</div>", unsafe_allow_html=True)
