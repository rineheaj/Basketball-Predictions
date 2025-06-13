import streamlit as st
import pandas as pd
from sim_core import (
    execute_simulation,
    render_simulation_metrics,
    get_team_stats
)
from team_images import show_team_bg_improved
from styles import (
    render_main_header,
    render_system_info_button,
    render_simulation_results,
    inject_custom_styles
)



def main():
    render_system_info_button()
    inject_custom_styles()
    render_main_header()
    
    st.sidebar.header("Sim Settings")
    num_sims = st.sidebar.slider(
        "Number of Simulations",
        min_value=100,
        max_value=50_000,
        step=1000,
        value=500
    )
    
    stats = get_team_stats()
    if not stats:
        return

    team_names = list(stats.keys())
    team1 = st.sidebar.selectbox("Select Team 1", team_names, index=0, key="team1")
    team2 = st.sidebar.selectbox(
        "Select Team 2",
        team_names,
        index=1 if team_names[0] == team1 else 0,
        key="team2"
    )
    
    show_team_bg_improved(teams=[team1, team2])
    
    if st.sidebar.button("Run Simulation"):
        results, game_log, analysis = execute_simulation(team1, team2, stats, num_sims)
        render_simulation_results(team1, team2, num_sims, results, game_log, analysis)
    
    if st.session_state.get("sim_run", False):
        results = st.session_state["results"]
        game_log = st.session_state["game_log"]
        analysis = st.session_state["analysis"]
        render_simulation_metrics(team1, team2, num_sims, analysis, results, game_log)


if __name__ == "__main__":
    main()