from rich.table import Table
from rich.console import Console
from rich import box

console = Console()

def log_simulations(team1, team2, game_log, limit=10):
    table = Table(
        title=f"[bold blue]🏀 Simulation Results: {team1} vs {team2}[/bold blue]",
        header_style="bold white on dark_blue",
        box=box.DOUBLE_EDGE,
        show_lines=True,
    )

    table.add_column(f"[cyan]{team1}[/cyan] Score", justify="right")
    table.add_column(f"[magenta]{team2}[/magenta] Score", justify="right")
    table.add_column("🏆 Winner", justify="center", style="bold green")

    for t1_score, t2_score, winner in game_log[:limit]:
        if winner == team1:
            win_style = "cyan"
        else:
            win_style = "magenta"

        table.add_row(
            str(t1_score),
            str(t2_score),
            f"[{win_style}]{winner}[/{win_style}]"
        )

    console.print(table)



