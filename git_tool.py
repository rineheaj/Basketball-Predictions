import subprocess
import webbrowser


def run_shell(cmd):
    print(f"\nRunning command: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Command failed with exit code: {result.returncode}.\nBye for now.")
        exit(1)


def yes_no(message):
    while (ans := input(f"{message} (y/n)").strip().lower()) not in ("y", "n"):
        print("Oops, please enter y or n")
    return ans == "y"


def main():
    print("=== Git Helper ===")

    if yes_no("Switch to 'main' branch?"):
        run_shell("git checkout main")
    else:
        print("Skipping branch switch, please make sure you are on correct branch.")
    

    if yes_no("Pull latest changes from 'origin/main'?"):
        run_shell("git pull origin main")
    else:
        print("Skipping Git pull, local 'main' might be outdated.")
    

    create_branch = yes_no("Create and switch to a new branch? ")
    if create_branch:
        branch_name = input("Enter a new branch name: ").strip()
        if branch_name == "":
            print(f"Branch name cannot be empty, bye for now.")
            exit(1)
        run_shell(f"git checkout -b {branch_name}")
    else:
        branch_name = None


    commit_changes = yes_no("Do you want to commit changes now? ")
    if commit_changes:
        run_shell("git status")

        commit_message = input("Enter commit message: ").strip()
        if commit_message == "":
            print("Commit message cannot be empty, bye for now.")
            exit(1)
        

        run_shell("git add .")
        run_shell(f'git commit -m "{commit_message}"')
    else:
        print("Skipping commit step.")
    
    branch_to_push = branch_name if branch_name is not None else "main"
    push_branch = yes_no(f"Push branch {branch_to_push} to origin?")
    if push_branch:
        run_shell(f"git push origin {branch_to_push}")
    else:
        print("Skipping push, your changes are only local.")
    

    if branch_name and push_branch:
        open_pr = yes_no("Open GitHub Pull Request page in broswer?")
        if open_pr:
            github_user = "rineheaj"
            repo_name = "Basketball-Predictions"
            pr_url = f"https://github.com/{github_user}/{repo_name}/pull/new/{branch_name}"
            print(f"Opening {pr_url}")
            webbrowser.open(pr_url)
        else:
            print(f"Skipped opening PR page.")
    
    print("\nNice one!")



if __name__ == "__main__":
    main()
