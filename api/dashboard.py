import streamlit as st
import pandas as pd
import plotly.express as px
from database.db_connection import connect_db

def show_team_dashboard():
    st.title("🌍 Team-Wise Analytics Dashboard")
    st.write("Analyze total runs, wickets, and player distribution across different teams.")
    
    # Connect to DB
    conn = connect_db()
    
    try:
        # Fetch data
        df = pd.read_sql("SELECT name as Name, team as Team, role as Role, runs as Runs, wickets as Wickets FROM players", conn)
        
        if df.empty or 'Team' not in df.columns:
            st.warning("No player data available. Please add players first.")
            return
            
        # Grouping dynamically by Team
        team_stats = df.groupby('Team').agg(
            Total_Runs=('Runs', 'sum'),
            Total_Wickets=('Wickets', 'sum'),
            Player_Count=('Name', 'count')
        ).reset_index()

        st.write("---")

        # --- Row for Teams ---
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            # Bar Chart for Team Runs
            fig_team_runs = px.bar(team_stats.sort_values('Total_Runs', ascending=False), 
                                   x='Team', y='Total_Runs', color='Team', 
                                   title="🏁 Total Runs by Team", text_auto=True)
            fig_team_runs.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
            st.plotly_chart(fig_team_runs, use_container_width=True)
            
        with col_t2:
            # Pie Chart for Player Count
            fig_team_count = px.pie(team_stats, names='Team', values='Player_Count', 
                                    title="👥 Player Count by Team", hole=0.4)
            st.plotly_chart(fig_team_count, use_container_width=True)

        st.write("---")
        
        # Sunburst Chart for Team Role Split
        st.subheader("📊 Role Breakdown per Team")
        fig_team_roles = px.sunburst(df, path=['Team', 'Role'], 
                                     title="Inner Circle = Team, Outer Circle = Role Segment")
        st.plotly_chart(fig_team_roles, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
    finally:
        conn.close()
