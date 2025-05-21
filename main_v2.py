import streamlit as st
import csv
import random
import pandas as pd


def load_team_stats(filename):
    stats = {}
    with open(filename, newline="") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            stats[row["Team"]] = {
                "ppg": float(row["PPG"]),
                "oppg": float(row["OPPG"])
            }
    return stats


def simulate_game(team1, team2, stats):
    t1 = stats[team1]
    t2 = stats[team2]
    t1_expected_outcome = (t1["ppg"] + t2["oppg"]) / 2
    t2_expected_outcome = (t2["ppg"] + t1["oppg"]) / 2
    t1_score = round(random.gauss(t1_expected_outcome, 12))
    t2_score = round(random.gauss(t2_expected_outcome, 12))
    winner = team1 if t1_score > t2_score else team2
    return winner, t1_score, t2_score


def run_sims(team1, team2, stats, num_sims=1000):
    results = {team1: 0, team2: 0}
    game_log = []
    for _ in range(num_sims):
        winner, t1_score, t2_score = simulate_game(team1, team2, stats)
        results[winner] += 1
        game_log.append((t1_score, t2_score, winner))
    return results, game_log


def main():
    st.title("🏀 NBA Simulation Predictor")
    st.markdown("This app simulates NBA games between two teams based on their offensive (PPG) and defensive (OPPG) statistics.")

    st.sidebar.header("Settings")

    num_sims = st.sidebar.slider("Number of Simulations", 100, 5000, 1000, 100)

    if "sim_ran" not in st.session_state:
        st.session_state.sim_ran = False

    try:
        stats = load_team_stats("nba_teams_2024.csv")
    except Exception as e:
        st.error(f"Error loading team stats: {e}")
        return

    team_names = list(stats.keys())
    if not team_names:
        st.error("No teams loaded, please check the CSV file.")
        return

    team1 = st.sidebar.selectbox("Select Team 1", team_names, index=0)
    defualt_index = 1 if len(team_names) > 1 and team_names[0] == team1 else 0
    team2 = st.sidebar.selectbox("Select Team 2", team_names, index=defualt_index)

    if st.sidebar.button("Run Simulation"):
        st.session_state.sim_ran = True
        st.session_state.results, st.session_state.game_log = run_sims(team1, team2, stats, num_sims)
        st.session_state.num_sims_used = num_sims

    if st.session_state.sim_ran:
        results = st.session_state.results
        game_log = st.session_state.game_log
        num_sims_used = st.session_state.num_sims_used

        st.subheader("Win Percentages")

        if team1 in results and team2 in results:
            st.write(f"{team1} Win Chance: {results[team1] / num_sims_used * 100:.1f}%")
            st.write(f"{team2} Win Chance: {results[team2] / num_sims_used * 100:.1f}%")
        else:
            st.info("Press Run Simulation button again to see accurate percentages.")
        
        st.subheader("Simulation Log")

        t1_scores = [log[0] for log in game_log]
        t2_scores = [log[1] for log in game_log]

        st.write("Histogram of Scores")
        score_data = pd.DataFrame({
            f"{team1} Score": t1_scores,
            f"{team2} Score": t2_scores,
        })
        st.bar_chart(score_data)


if __name__ == "__main__":
    main()
