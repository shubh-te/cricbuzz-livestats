import streamlit as st
import pandas as pd
from database.db_connection import connect_db

def render_crud_players():
    st.header("⚙️ Player Management (CRUD)")
    st.write("Add, View, Update, or Delete player records from the database.")

    conn = connect_db()
    cursor = conn.cursor()

    # Create Tabs for CRUD operations
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Player", "📖 View Players", "✏️ Update Player", "❌ Delete Player"])

    # --- 1. ADD PLAYER (CREATE) ---
    with tab1:
        st.subheader("Add a New Player")
        with st.form("add_player_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("Player Name")
                new_role = st.selectbox("Role", ["Batsman", "Bowler", "All-Rounder", "Wicket-Keeper"])
            with col2:
                new_runs = st.number_input("Runs", min_value=0, value=0, step=10)
                new_wickets = st.number_input("Wickets", min_value=0, value=0, step=1)
            
            submit_add = st.form_submit_button("Save Player")
            if submit_add:
                if new_name.strip() == "":
                    st.error("Player name cannot be empty!")
                else:
                    try:
                        cursor.execute("INSERT INTO players (name, role, runs, wickets) VALUES (?, ?, ?, ?)", 
                                       (new_name, new_role, new_runs, new_wickets))
                        conn.commit()
                        st.success(f"Player '{new_name}' added successfully! 🎉")
                    except Exception as e:
                        st.error(f"Error adding player: {e}")

    # --- 2. VIEW PLAYERS (READ) ---
    with tab2:
        st.subheader("All Players in Database")
        try:
            df = pd.read_sql("SELECT name as Name, role as Role, runs as Runs, wickets as Wickets FROM players", conn)
            if df.empty:
                st.info("No players found in the database. Please add some!")
            else:
                # Add a proper Serial Number starting from 1
                df.insert(0, "S.No", range(1, len(df) + 1))
                st.dataframe(df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Error fetching data: {e}")

    # --- 3. UPDATE PLAYER (UPDATE) ---
    with tab3:
        st.subheader("Update Existing Player")
        try:
            df_update = pd.read_sql("SELECT id, name FROM players", conn)
            if df_update.empty:
                st.info("No players available to update.")
            else:
                # Create a dictionary mapping name -> id for the selectbox
                player_dict = dict(zip(df_update['name'], df_update['id']))
                selected_player_name = st.selectbox("Select Player to Update", list(player_dict.keys()), key="update_select")
                selected_id = player_dict[selected_player_name]

                # Fetch current stats
                cursor.execute("SELECT role, runs, wickets FROM players WHERE id=?", (selected_id,))
                current_data = cursor.fetchone()

                if current_data:
                    with st.form("update_player_form"):
                        col1, col2 = st.columns(2)
                        with col1:
                            upd_role = st.selectbox("Role", ["Batsman", "Bowler", "All-Rounder", "Wicket-Keeper"], 
                                                    index=["Batsman", "Bowler", "All-Rounder", "Wicket-Keeper"].index(current_data[0]) if current_data[0] in ["Batsman", "Bowler", "All-Rounder", "Wicket-Keeper"] else 0)
                        with col2:
                            upd_runs = st.number_input("Runs", min_value=0, value=current_data[1], step=10)
                            upd_wickets = st.number_input("Wickets", min_value=0, value=current_data[2], step=1)
                        
                        submit_update = st.form_submit_button("Update Player")
                        if submit_update:
                            cursor.execute("UPDATE players SET role=?, runs=?, wickets=? WHERE id=?", 
                                           (upd_role, upd_runs, upd_wickets, selected_id))
                            conn.commit()
                            st.success(f"Player '{selected_player_name}' updated successfully! ✅")
        except Exception as e:
            st.error(f"Error: {e}")

    # --- 4. DELETE PLAYER (DELETE) ---
    with tab4:
        st.subheader("Delete Player")
        try:
            df_delete = pd.read_sql("SELECT id, name FROM players", conn)
            if df_delete.empty:
                st.info("No players available to delete.")
            else:
                player_dict_del = dict(zip(df_delete['name'], df_delete['id']))
                del_player_name = st.selectbox("Select Player to Delete", list(player_dict_del.keys()), key="del_select")
                del_id = player_dict_del[del_player_name]

                st.warning(f"Are you sure you want to delete **{del_player_name}**? This action cannot be undone.")
                
                if st.button("🚨 Yes, Delete Player", type="primary"):
                    cursor.execute("DELETE FROM players WHERE id=?", (del_id,))
                    conn.commit()
                    st.success(f"Player '{del_player_name}' deleted successfully! 🗑️")
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    render_crud_players()