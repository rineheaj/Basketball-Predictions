import csv
from rich import print
from rich.console import Console
from rich.table import Table
from pathlib import Path



console = Console()

def load_validate_csv_teams(filename: str):
    file_path = Path(filename)

    if file_path.exists() and file_path.is_file() and file_path.suffix == ".csv":
        with file_path.open(mode="r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            missing_data_comp = [
                (file_path.name, row.get("Model", "No Car"), col) for row in reader for col, value in row.items() if not value or not value.strip()
            ]


    if missing_data_comp:
        table = Table(title="[bold magenta]🚨 Missing Data Report 🚨[/bold magenta]")
        table.add_column("[cyan]Filename[/cyan]", style="cyan", justify="center")
        table.add_column("[magenta]Model[/magenta]", style="magenta", justify="center")
        table.add_column("[red]Column[/red]", style="red", justify="center")

        for entry in missing_data_comp:
            table.add_row(*entry)
        print()
        console.print(table)
        print()
    else:
        console.print("[green] No missing data was found.[/green]")


if __name__ == "__main__":
    load_validate_csv_teams(
        filename="Electric_Vehicle_Population_Data.csv"
    )

