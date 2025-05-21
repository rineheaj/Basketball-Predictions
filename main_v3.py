import streamlit as st
import pandas as pd
from sim_core import (
    load_team_stats, run_sim, quick_analysis
)


def main():
    st.title("🏀 NBA Simulation Predictor")
    st.sidebar.header("Settings")

    num_sims = st.sidebar.slider(
        "Number of Simulations",
        min_value=100,
        max_value=5000,
        step=100,
        value=500
    )

    try:
        stats = load_team_stats("nba_teams_2024.csv")
    except Exception as e:
        st.error(f"Error loading team stats: {e}")
        return

    team_names = list(stats.keys())
    team1 = st.sidebar.selectbox(
        "Select Team 1",
        team_names,
        index=0,
        key="team1"
    )

    team2 = st.sidebar.selectbox(
        "Select Team 2",
        team_names,
        index=1 if team_names[0] == team1 else 0,
        key="team2"
    )



    if st.sidebar.button("Run Simulation"):
        with st.spinner("Running sims..."):
            results, game_log = run_sim(
                team1, team2, stats, num_sims
            )
            analysis = quick_analysis(
                game_log=game_log,
                team1=team1,
                team2=team2
            )

            df_2 = pd.DataFrame(
                data=game_log,
                columns=["Team 1 Score", "Team 2 Score", "Winner"]
            )
            st.dataframe(df_2)

            st.session_state["results"] = results
            st.session_state["game_log"] = game_log
            st.session_state["analysis"] = analysis
            st.session_state["sim_run"] = True

    if st.session_state.get("sim_run", False):
        team1 = st.session_state["team1"]
        team2 = st.session_state["team2"]
        results = st.session_state["results"]
        game_log = st.session_state["game_log"]
        analysis = st.session_state["analysis"]

        # Check if selected teams are in results
        if team1 in results and team2 in results:
            st.subheader("Win Chance 🏆")
            st.write(
                f"{team1} Win Chance: {results.get(team1, 0) / num_sims * 100:.1f}%"
            )
            st.write(
                f"{team2} Win Chance: {results.get(team2, 0) / num_sims * 100:.1f}%"
            )

            st.subheader("🧾Average Scores & Insights")
            st.write(
                f"Average {team1} Score: {analysis['avg_scores'].get(team1, 0):.1f}"
            )
            st.write(
                f"Average {team2} Score: {analysis['avg_scores'].get(team2, 0):.1f}"
            )
            st.write(
                f"Average Point Differential: {analysis.get('point_diff', 0):.1f}"
            )
            st.write(
                f"Close Games (<=5 points): {analysis.get('close_games', 0)}"
            )

            st.subheader("📊Score Distribution")
            df = pd.DataFrame(
                {
                    f"{team1} Score": [log[0] for log in game_log],
                    f"{team2} Score": [log[1] for log in game_log]
                }
            )
            st.bar_chart(
                df,
                x_label="Number of Sims",
                y_label="Total Points Scored",
                use_container_width=True
            )
        else:
            st.warning("Please re-run the simulation after changing teams.")

if __name__ == "__main__":
    main()
