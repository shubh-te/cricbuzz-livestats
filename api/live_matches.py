import streamlit as st
from api.fetch_data import get_live_matches

def render_live_matches():
    st.header("📡 Live Cricket Scores")
    st.write("Real-time updates directly from the stadium! 🚀")
    
    matches = get_live_matches()

    if not matches:
        st.warning("No live data available currently or Invalid API Key.")
        return

    # Check for error from API
    if "error" in matches[0]:
        st.error(f"API Error/Note: {matches[0]['error']}")
        return

    # Extract all unique match types (like 'Test', 'ODI', 'T20') and add an 'All' option
    match_types = ["All"] + sorted(list(set([m.get("matchType", "Unknown") for m in matches])))
    
    # 🔥 Create Streamlit Tabs for Match Categories
    tabs = st.tabs(match_types)
    
    for tab, m_type in zip(tabs, match_types):
        with tab:
            # Filter matches according to the current tab
            if m_type == "All":
                filtered_matches = matches
            else:
                filtered_matches = [m for m in matches if m.get("matchType", "Unknown") == m_type]

            # Adding a clean Subheader for the tab to display total count
            st.markdown(f"### {m_type} Matches ({len(filtered_matches)})")

            if not filtered_matches:
                st.info(f"No {m_type} matches available right now.")
                continue

            # Creating a Grid Layout for Filtered Matches
            col1, col2 = st.columns(2)
            
            for i, match in enumerate(filtered_matches):
                match_name = match.get("name", "Unknown Match")
                venue = match.get("venue", "Venue Unknown")
                match_type_label = match.get("matchType", "Unknown Type")
                date = match.get("date", "Unknown Date")
                status = match.get("status", "Status Unknown")
                scores = match.get("score", [])

                # Assigning column alternately (Left then Right)
                col = col1 if i % 2 == 0 else col2
                
                with col:
                    # Using Streamlit Container to create a Box/Card like Google Scorecard
                    with st.container(border=True):
                        st.markdown(f"#### 🏏 {match_name}")
                        st.caption(f"**{match_type_label}** • 🏟️ {venue} • 📅 {date}")
                        
                        st.markdown("---")
                        
                        if scores:
                            for s in scores:
                                inning_name = s.get("inning", "Inning")
                                runs = s.get("r", 0)
                                wickets = s.get("w", 0)
                                overs = s.get("o", 0.0)
                                
                                # Google Style Score Formatting
                                st.markdown(f"**{inning_name}**: &nbsp;&nbsp;&nbsp; <span style='font-size: 20px; font-weight: bold; color: #1f77b4;'>{runs}/{wickets}</span> <span style='opacity:0.7;'>({overs} ov)</span>", unsafe_allow_html=True)
                        else:
                            st.info("Match hasn't started yet or Score not available.")
                        
                        st.markdown("---")
                        st.markdown(f"<p style='color:#ff4b4b; font-weight:bold;'>📌 {status}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    render_live_matches()