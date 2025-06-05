import subprocess
import webbrowser
from sys import exit
from typing import NamedTuple

class GitHubSettings(NamedTuple):
    username: str
    repo_name: str

gh_settings = GitHubSettings(
    username="rineheaj".lower(),
    repo_name="basketball-predictions".lower()
)

def run_hell(cmd):
    print(f"\nRunning command: {cmd}")
    if (result := subprocess.run(cmd, shell=True)).returncode != 0:
        print(f"Command failed with exit code: {result.returncode}.\nBye for now.")
        exit(1)

def handle_commit():
    run_hell("git status")
    if not (commit_message := input("Enter commit message: ").strip()):
        print("Commit message cannot be empty, bye for now.")
        exit(1)
    run_hell("git add .")
    run_hell(f'git commit -m "{commit_message}"')


def non_empty(msg):
    while not (value := input(msg).strip()):
        print("Input cannot be empty, please try that again.")
    return value

def yes_no(msg):
    while (ans := input(f"{msg} (y/n)").strip().lower()) not in ("y", "n"):
        print("Oops, please enter y or n")
    return ans == "y"

def maybe_open_pr(branch_name, push_branch):
    if branch_name and push_branch and (pr_url := f"https://github.com/{gh_settings.username}/{gh_settings.repo_name}/pull/new/{branch_name}"):
        if yes_no("Open PR? "):
            print(f"Opening {pr_url}")
            webbrowser.open(pr_url)
        else:
            print("Skipped opening PR page.")


def main():
    print("=== Git Helper ===")

    if yes_no("Switch to 'main' branch?"):
        run_hell("git checkout main")
    else:
        print("Skipping branch switch, please make sure you are on correct branch.")
    

    if yes_no("Pull latest changes from 'origin/main'?"):
        run_hell("git pull origin main")
    else:
        print("Skipping Git pull, local 'main' might be outdated.")
    

    create_branch = yes_no("Create and switch to a new branch? ")
    if create_branch:
        branch_name = non_empty("Enter a new branch name: ")
        run_hell(f"git checkout -b {branch_name}")
    else:
        branch_name = None


    if yes_no("Do you want to commit changes now? "):
        handle_commit()
    else:
        print("Skipping commit step.")
    
    branch_to_push = branch_name if branch_name is not None else "main"
    push_branch = yes_no(f"Push branch {branch_to_push} to origin?")
    if push_branch:
        run_hell(f"git push origin {branch_to_push}")
    else:
        print("Skipping push, your changes are only local.")

    maybe_open_pr(branch_name, push_branch)
    print("\nNice one!")


if __name__ == "__main__":
    main()
