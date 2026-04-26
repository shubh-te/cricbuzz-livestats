import streamlit as st
from database.db_connection import connect_db
from api.ml_prediction import render_ml_page

st.set_page_config(page_title="Cricbuzz LiveStats PRO", layout="wide")

st.title("🏏 Cricbuzz LiveStats Dashboard")
st.write("Welcome to the Cricket Analytics Dashboard!")

# Navigation
menu = st.sidebar.selectbox("Navigation", ["Home", "Live Match", "Team Dashboard", "Player Analytics", "SQL Pro Analytics", "Manage Players (CRUD)", "ML Predictions"])

conn = connect_db()
with open("database/schema.sql", "r") as f:
    conn.executescript(f.read())
    
# Safely add 'team' column if it doesn't exist
try:
    conn.execute("ALTER TABLE players ADD COLUMN team TEXT DEFAULT 'Unknown'")
except Exception:
    pass

if menu == "Home":
    st.markdown("---")
    st.markdown("### 🏆 Welcome to the Ultimate Cricket Analytics Hub")
    st.write("Get real-time match updates, deep-dive player analytics, and build SQL/ML predictions all in one place!")
    
    # 📊 Quick Stats Overview
    try:
        total_players = conn.execute("SELECT COUNT(*) FROM players").fetchone()[0]
        total_runs = conn.execute("SELECT SUM(runs) FROM players").fetchone()[0]
        total_wickets = conn.execute("SELECT SUM(wickets) FROM players").fetchone()[0]
        top_scorer = conn.execute("SELECT name FROM players ORDER BY runs DESC LIMIT 1").fetchone()
        top_scorer_name = top_scorer[0] if top_scorer else "N/A"
        
        st.write("#### 📈 Database Overview")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Players Added", total_players)
        c2.metric("Total Runs Scored", f"{total_runs:,}" if total_runs else "0")
        c3.metric("Total Wickets Taken", f"{total_wickets:,}" if total_wickets else "0")
        c4.metric("All-time Top Scorer", top_scorer_name)
    except Exception:
        pass
        
    st.markdown("---")
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.info("🔴 **Live Matches**\n\nGet live Google-like scorecard updates with real-time data.")
        st.warning("🌍 **Team Dashboard**\n\nAnalyze team strengths and total runs across countries.")
        st.success("⚙️ **Manage Players (CRUD)**\n\nFull control to add, edit, or delete any player in the DB.")
        
    with res_col2:
        st.success("📊 **Player Analytics**\n\nVisualize player rankings and career stats with interactive Plotly charts.")
        st.error("🤖 **ML Predictions**\n\nPredict match win probabilities using Logistic Regression models.")
        st.info("💻 **SQL Pro Analytics**\n\nRun your own custom SQL queries directly against our SQLite tables.")
elif menu == "Live Match":
    from api.live_matches import render_live_matches
    render_live_matches()
elif menu == "Team Dashboard":
    from api.dashboard import show_team_dashboard
    show_team_dashboard()
elif menu == "Player Analytics":
    from api.player_stats import render_player_analytics
    render_player_analytics()
elif menu == "SQL Pro Analytics":
    from api.sql_analytics import render_sql_analytics
    render_sql_analytics()
elif menu == "Manage Players (CRUD)":
    from api.crud_players import render_crud_players
    render_crud_players()
elif menu == "ML Predictions":
    render_ml_page()