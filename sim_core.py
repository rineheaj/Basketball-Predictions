import csv
import random


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


def simulate_game(team1, team2, stats):
    t1_stats = stats[team1]
    t2_stats = stats[team2]

    t1_expected = (t1_stats["ppg"] + t2_stats["oppg"]) / 2
    t2_expected = (t2_stats["ppg"] + t1_stats["oppg"]) / 2

    t1_score = round(random.gauss(t1_expected, 6))
    t2_score = round(random.gauss(t2_expected, 6))

    winner = team1 if t1_score > t2_score else team2
    return winner, t1_score, t2_score


def run_sim(team1, team2, stats, num_sims=1000):
    results = {team1: 0, team2: 0}
    game_log = []

    for _ in range(num_sims):
        winner, t1_score, t2_score = simulate_game(
            team1, team2, stats
        )
        results[winner] += 1
        game_log.append((t1_score, t2_score, winner))

    return results, game_log


def quick_analysis(game_log, team1, team2):
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

def highest_score(game_log):
    for log in game_log:
        print(f"LOG: {log}")


def highlight_winners(row, team1, team2):
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


