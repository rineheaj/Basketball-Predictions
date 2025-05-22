import csv

def main():
    new_teams = [
        ["Thunder", 115.40, 100.5],
        ["Timberwolves", 98.8, 105.40],
        ["Pacers", 115.4, 110.0],
        ["Knicks", 118, 111.4]
    ]

    infile = "nba_teams_2024.csv"

    with open(infile, mode="a", newline="") as outfile:
        try:
            outfile.write("\n")
            writer = csv.writer(outfile)
            writer.writerows(new_teams)
        except Exception as e:
            print(f"ERROR: {e}")

    print("Teams appended!")

if __name__ == "__main__":
    main()