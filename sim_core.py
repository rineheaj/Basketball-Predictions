import csv
import random
from decors import depricated
import streamlit as st
import pandas as pd
from typing import Optional, Any

@depricated
def load_team_stats(filename):
    stats = {}

    with open(filename, newline="") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            stats[row["Team"]] = {
                "ppg": float(row["PPG"]),
                "oppg": float(row["OPPG"]),
            }

    return stats


def load_team_stats_improved(filename: str) -> dict[str, dict[str, float]]:
    with open(filename, mode="r", newline="") as infile:
        reader = csv.DictReader(infile)

        stats: csv.DictReader = {
            row["Team"]: {"ppg": float(row["PPG"]), "oppg": float(row["OPPG"])}
            for row in reader
        }

    # for team in stats:
    #     st.write(
    #         f"{team} on average score {stats[team]['ppg']} and give up {stats[team]['oppg']}."
    #     )

    return stats



def simulate_game(team1: str, team2: str, stats: dict) -> tuple[str, int, int]:
    t1_stats = stats[team1]
    t2_stats = stats[team2]

    t1_expected = (t1_stats["ppg"] + t2_stats["oppg"]) / 2
    t2_expected = (t2_stats["ppg"] + t1_stats["oppg"]) / 2

    t1_score = round(random.gauss(t1_expected, 6))
    t2_score = round(random.gauss(t2_expected, 6))

    winner = team1 if t1_score > t2_score else team2
    return winner, t1_score, t2_score


def run_sim(team1: str, team2: str, stats: dict, num_sims: int =1000) -> tuple[dict[str, int], list[tuple[int, int, str]]]:
    results = {team1: 0, team2: 0}
    game_log = []

    for _ in range(num_sims):
        winner, t1_score, t2_score = simulate_game(
            team1, team2, stats
        )
        results[winner] += 1
        game_log.append((t1_score, t2_score, winner))

    return results, game_log


def quick_analysis(game_log: list[tuple], team1: str, team2: str) -> dict[str, Any]:
    total_t1 = sum(
        t1 for t1, _, _ in game_log
    )
    
    total_t2 = sum(
        t2 for _, t2, _ in game_log
    )

    avg_t1 = total_t1 / len(game_log)
    avg_t2 = total_t2 / len(game_log)

    point_diff = avg_t1 - avg_t2

    close_games = sum(
        abs(t1 - t2) <= 5 for t1, t2, _ in game_log
    )

    return {
        "avg_scores": {
            team1: round(avg_t1, 1),
            team2: round(avg_t2, 1),
        },
        "point_diff": round(point_diff, 1),
        "close_games": close_games,
    }

@depricated
def highest_score(game_log):
    for log in game_log:
        print(f"LOG: {log}")


def highlight_winners(row: dict, team1: str, team2: str) -> list[str]:
    if row["Winner"] == team1:
        return [
            "background-color: lightblue"
        ] * len(row)
    elif row["Winner"] == team2:
        return [
            "background-color: lightcoral"
        ] * len(row)
    return [
        "" * len(row)
    ]


def lem_highlight_winners(row: dict, team1: str, team2: str) -> Optional[list[str]]:
    if row["Winner"] == team1:
        return ["background-color: limegreen; font-weight: bold; color: white"] * len(row)
    elif row["Winner"] == team2:
        return ["background-color: tomato; font-weight: bold; color: white"] * len(row)
    return [""] * len(row)


def get_team_stats() -> Optional[dict[str, dict[str, float]]]:
    try:
        return load_team_stats_improved("nba_teams_2024.csv")
    except Exception as e:
        st.error(f"Error loading team stats: {e}")
        return None


def execute_simulation(team1: str, team2: str, stats: dict, num_sims: int) -> tuple[dict[str, int], list[int, int, str], dict[str, Any]]:
    with st.spinner("Running sims..."):
        results, game_log = run_sim(team1, team2, stats, num_sims)
        analysis = quick_analysis(game_log=game_log, team1=team1, team2=team2)
    return results, game_log, analysis





def render_simulation_metrics(team1, team2, num_sims, analysis, results, game_log):
    if team1 in results and team2 in results:
        st.markdown('<h3 style="text-align: center;">🏆 Win Chance</h3>', unsafe_allow_html=True)
        st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label=f"{team1} Win Chance", value=f"{results.get(team1, 0) / num_sims * 100:.1f}%", border=True)
        with col2:
            st.metric(label=f"{team2} Win Chance", value=f"{results.get(team2, 0) / num_sims * 100:.1f}%", border=True)
    
        st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
        st.subheader("📊 Average Scores & Insights")
        st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
    
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label=f"Avg {team1} Score", value=f"{analysis['avg_scores'].get(team1, 0):.1f}", border=True)
        with col2:
            st.metric(label=f"Avg {team2} Score", value=f"{analysis['avg_scores'].get(team2, 0):.1f}", border=True)
        with col3:
            st.metric(label="Avg Point Differential", value=f"{analysis.get('point_diff', 0):.1f}", border=True)
    
        st.metric(label="Close Games (≤5 points)", value=f'{analysis.get("close_games", 0):,}', border=True)
        st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
    
        df_scores = pd.DataFrame({
            f"{team1} Score": [log[0] for log in game_log],
            f"{team2} Score": [log[1] for log in game_log]
        })
        st.bar_chart(df_scores, x_label="Number of Sims", y_label="Total Points Scored", use_container_width=True)
    else:
        st.warning("Please re-run the simulation after changing teams.")