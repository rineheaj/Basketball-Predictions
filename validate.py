import csv


def load_validate_csv_teams(filename: str):
    with open(filename, mode="r", newline="") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            team_name = row.get("Team", "Team went on vacation!")
            for col, data in row.items():
                if data is None or data.strip() =="":
                    print(f"There is missing data in {filename}, Team: {team_name}, Column: {col}")


if __name__ == "__main__":
    
    load_validate_csv_teams(
        filename="nba_teams_2024_test.csv"
    )

