import streamlit as st
import pandas as pd
import plotly.express as px
from database.db_connection import connect_db

def render_player_analytics():
    st.header("🏆 Player Analytics & Rankings")
    st.write("Calculcating advanced metric scores = (Runs + (Wickets * 20))")

    conn = connect_db()

    # ⭐ Auto-insert lots of superstars if database has very few players
    check_empty = pd.read_sql("SELECT COUNT(*) as count FROM players", conn)
    if check_empty["count"][0] <= 15:
        # Delete existing few records to insert a massive fresh list
        conn.execute("DELETE FROM players")
        
        seed_data = [
            # 🇮🇳 India
            ("Virat Kohli", "India", "Batsman", 26733, 4),
            ("Rohit Sharma", "India", "Batsman", 18820, 11),
            ("MS Dhoni", "India", "Wicket-Keeper", 17266, 1),
            ("Sachin Tendulkar", "India", "Batsman", 34357, 201),
            ("Jasprit Bumrah", "India", "Bowler", 420, 397),
            ("Mohammed Shami", "India", "Bowler", 510, 448),
            ("Ravindra Jadeja", "India", "All-Rounder", 6200, 568),
            ("R. Ashwin", "India", "All-Rounder", 4120, 744),
            ("Yuvraj Singh", "India", "All-Rounder", 11778, 148),
            ("Virender Sehwag", "India", "Batsman", 17253, 40),
            ("Rahul Dravid", "India", "Batsman", 24208, 1),
            ("Sourav Ganguly", "India", "Batsman", 18575, 132),
            ("Zaheer Khan", "India", "Bowler", 1100, 610),

            # 🇦🇺 Australia
            ("Ricky Ponting", "Australia", "Batsman", 27483, 5),
            ("Pat Cummins", "Australia", "Bowler", 1450, 461),
            ("Mitchell Starc", "Australia", "Bowler", 1200, 642),
            ("David Warner", "Australia", "Batsman", 18612, 0),
            ("Steve Smith", "Australia", "Batsman", 16225, 25),
            ("Glenn Maxwell", "Australia", "All-Rounder", 6450, 142),
            ("Adam Gilchrist", "Australia", "Wicket-Keeper", 15461, 0),
            ("Brett Lee", "Australia", "Bowler", 1120, 718),
            ("Glenn McGrath", "Australia", "Bowler", 700, 949),
            ("Shane Warne", "Australia", "Bowler", 3154, 1001),

            # 🏴󠁧󠁢󠁥󠁮󠁧󠁿 England
            ("Joe Root", "England", "Batsman", 18985, 52),
            ("Ben Stokes", "England", "All-Rounder", 10214, 320),
            ("James Anderson", "England", "Bowler", 1340, 987),
            ("Stuart Broad", "England", "Bowler", 3662, 847),
            ("Jos Buttler", "England", "Wicket-Keeper", 10830, 0),
            ("Eoin Morgan", "England", "Batsman", 10859, 0),
            ("Kevin Pietersen", "England", "Batsman", 13797, 10),

            # 🇵🇰 Pakistan
            ("Babar Azam", "Pakistan", "Batsman", 13325, 0),
            ("Mohammad Rizwan", "Pakistan", "Wicket-Keeper", 6700, 0),
            ("Shaheen Afridi", "Pakistan", "Bowler", 420, 288),
            ("Wasim Akram", "Pakistan", "Bowler", 3717, 916),
            ("Waqar Younis", "Pakistan", "Bowler", 1010, 789),
            ("Inzamam-ul-Haq", "Pakistan", "Batsman", 20580, 0),
            ("Shahid Afridi", "Pakistan", "All-Rounder", 11196, 541),

            # 🇿🇦 South Africa
            ("AB de Villiers", "South Africa", "Batsman", 20014, 2),
            ("Jacques Kallis", "South Africa", "All-Rounder", 25534, 577),
            ("Dale Steyn", "South Africa", "Bowler", 1251, 699),
            ("Kagiso Rabada", "South Africa", "Bowler", 930, 502),
            ("Hashim Amla", "South Africa", "Batsman", 18672, 0),

            # 🇳🇿 New Zealand
            ("Kane Williamson", "New Zealand", "Batsman", 18128, 30),
            ("Trent Boult", "New Zealand", "Bowler", 650, 602),
            ("Ross Taylor", "New Zealand", "Batsman", 18199, 2),
            ("Tim Southee", "New Zealand", "Bowler", 2150, 765),
            ("Daniel Vettori", "New Zealand", "All-Rounder", 6989, 705),

            # 🏝️ West Indies
            ("Chris Gayle", "West Indies", "Batsman", 19593, 260),
            ("Brian Lara", "West Indies", "Batsman", 22358, 0),
            ("Kieron Pollard", "West Indies", "All-Rounder", 4275, 97),
            ("Jason Holder", "West Indies", "All-Rounder", 6100, 401),
            ("Kemar Roach", "West Indies", "Bowler", 1000, 412),

            # 🇱🇰 Sri Lanka & Others
            ("Kumar Sangakkara", "Sri Lanka", "Wicket-Keeper", 28016, 0),
            ("Mahela Jayawardene", "Sri Lanka", "Batsman", 25957, 14),
            ("Lasith Malinga", "Sri Lanka", "Bowler", 1000, 546),
            ("Muttiah Muralitharan", "Sri Lanka", "Bowler", 1936, 1347),
            ("Rashid Khan", "Afghanistan", "Bowler", 1550, 521),
            ("Shakib Al Hasan", "Bangladesh", "All-Rounder", 14321, 690),
            ("Tamim Iqbal", "Bangladesh", "Batsman", 15200, 0)
        ]
        
        conn.executemany("INSERT INTO players (name, team, role, runs, wickets) VALUES (?, ?, ?, ?, ?)", seed_data)
        conn.commit()

    try:
        # Fetch data
        df = pd.read_sql("SELECT name as Name, team as Team, role as Role, runs as Runs, wickets as Wickets FROM players", conn)
        
        if df.empty:
            st.warning("No player data available")
        else:
            # KPI Dashboard - Pehle jaisa (Top Performers)
            st.subheader("📊 Top Performers Dashboard")
            col1, col2, col3 = st.columns(3)
            with col1:
                top_scorer = df.sort_values(by="Runs", ascending=False).iloc[0]
                st.metric("🏏 Top Batsman", top_scorer["Name"], f"{top_scorer['Runs']} Runs")
            with col2:
                top_wicket = df.sort_values(by="Wickets", ascending=False).iloc[0]
                st.metric("🎯 Top Bowler", top_wicket["Name"], f"{top_wicket['Wickets']} Wickets")
            with col3:
                # Calculate simple MVP for All-Rounder
                df['Points'] = df['Runs'] + (df['Wickets'] * 20)
                best_ar = df[df['Role'] == 'All-Rounder'].sort_values(by="Points", ascending=False).iloc[0]
                st.metric("⚔️ Top All-Rounder", best_ar["Name"], f"{best_ar['Runs']} R | {best_ar['Wickets']} W")

            st.write("---")
            st.subheader("📈 Visual Analytics Dashboard")
            
            # --- Graph Row 1 ---
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                # Top 10 Runs Bar Chart
                top_batsmen = df.sort_values(by="Runs", ascending=False).head(10)
                fig_runs = px.bar(top_batsmen, x='Name', y='Runs', color='Runs', 
                                  title="🏏 Top 10 Run Scorers", text_auto='.2s', color_continuous_scale="Blues")
                fig_runs.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
                st.plotly_chart(fig_runs, use_container_width=True)

            with col_chart2:
                # Top 10 Wickets Bar Chart
                top_bowlers = df.sort_values(by="Wickets", ascending=False).head(10)
                fig_wickets = px.bar(top_bowlers, x='Name', y='Wickets', color='Wickets', 
                                     title="🎯 Top 10 Wicket Takers", text_auto='.2s', color_continuous_scale="Reds")
                fig_wickets.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
                st.plotly_chart(fig_wickets, use_container_width=True)

            # --- Graph Row 2 ---
            col_chart3, col_chart4 = st.columns(2)
            
            with col_chart3:
                # Role Distribution Pie Chart
                fig_roles = px.pie(df, names='Role', hole=0.4, title="🧩 Role Distribution (Batter/Bowler/All-Rounder)", 
                                   color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig_roles, use_container_width=True)
                
            with col_chart4:
                # Scatter Bubble Chart for MVP Analysis
                fig_scatter = px.scatter(df, x='Runs', y='Wickets', color='Role', size='Points', hover_name='Name',
                                         title="⭐ Runs vs Wickets (Bubble Size = MVP Points)")
                st.plotly_chart(fig_scatter, use_container_width=True)
            st.write('---')
            st.subheader('📋 Complete Player List')

            
            # Teeno ko alag kiya (Tabs)
            tab1, tab2, tab3, tab4 = st.tabs(["All Players", "🏏 Batsmen", "🎯 Bowlers", "⚔️ All-Rounders"])

            with tab1:
                df_all = df.drop(columns=['Points'])
                df_all.insert(0, "S.No", range(1, len(df_all) + 1))
                st.dataframe(df_all, use_container_width=True, hide_index=True)
            
            with tab2:
                df_bat = df[df['Role'] == 'Batsman'].drop(columns=['Points']).reset_index(drop=True)
                df_bat.insert(0, "S.No", range(1, len(df_bat) + 1))
                st.dataframe(df_bat, use_container_width=True, hide_index=True)

            with tab3:
                df_bowl = df[df['Role'] == 'Bowler'].drop(columns=['Points']).reset_index(drop=True)
                df_bowl.insert(0, "S.No", range(1, len(df_bowl) + 1))
                st.dataframe(df_bowl, use_container_width=True, hide_index=True)

            with tab4:
                df_ar = df[df['Role'] == 'All-Rounder'].drop(columns=['Points']).reset_index(drop=True)
                df_ar.insert(0, "S.No", range(1, len(df_ar) + 1))
                st.dataframe(df_ar, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error fetching data: {e}")

if __name__ == "__main__":
    render_player_analytics()