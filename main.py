import csv
import random
from logger import log_simulations



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

    return (
        winner,
        t1_score,
        t2_score
    )

def run_sims(team1, team2, stats, num_sims=1000):
    results = {team1: 0, team2: 0}

    game_log = []

    for _ in range(num_sims):
        winner, t1_score, t2_score = simulate_game(
            team1,
            team2,
            stats
        )
        results[winner] += 1
        game_log.append((t1_score, t2_score, winner))

    return results, game_log







def main():
    stats = load_team_stats("nba_teams_2024.csv")

    team1 = "Celtics"
    team2 = "Nuggets"

    results, game_log = run_sims(
        team1, team2, stats
    )

    print(f"After 1000 simulations:")
    
    for team in [team1, team2]:
        print(f"{team}: {results[team] / 10:.1f}% win chance")

    log_simulations(
        team1, team2, game_log
    )


if __name__ == "__main__":
    main()
