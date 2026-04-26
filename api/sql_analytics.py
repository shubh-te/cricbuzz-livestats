import streamlit as st
import pandas as pd
import plotly.express as px
from database.db_connection import connect_db

def render_sql_analytics():
    st.title("🧮 Advanced SQL Analytics & Charts")

    conn = connect_db()

    # Pre-defined Advanced Queries
    advanced_queries = {
        "Custom Query": "",
        "Top 5 Batsmen by Runs": "SELECT name, runs FROM players ORDER BY runs DESC LIMIT 5",
        "Team Average Scores": "SELECT team1, COUNT(*) as matches_played FROM matches GROUP BY team1",
        "Player Ranking (Runs + Wickets * 20)": "SELECT name, (runs + (wickets * 20)) as ranking_points FROM players ORDER BY ranking_points DESC LIMIT 10"
    }

    query_choice = st.selectbox("Select an Advanced Query or Write your own", list(advanced_queries.keys()))
    query = st.text_area("SQL query:", value=advanced_queries[query_choice])

    if st.button("Run Analytics"):
        try:
            result = pd.read_sql(query, conn)
            st.dataframe(result)
            
            # Determine Visualization
            if len(result.columns) >= 2:
                st.subheader("Visual Analytics (Plotly)")
                col1 = result.columns[0]
                col2 = result.columns[1]
                if pd.api.types.is_numeric_dtype(result[col2]):
                    fig = px.bar(result, x=col1, y=col2, title=f"{col2} by {col1}", color=col2, color_continuous_scale="Viridis")
                    st.plotly_chart(fig, use_container_width=True)
                    
        except Exception as e:
            st.error(f"Error: {e}")

# Enable direct script run or import via Streamlit
if __name__ == "__main__":
    render_sql_analytics()