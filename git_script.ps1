param (
    [string]$CommitMessage = "Some styling changes..."
)

git add .

git commit -m $CommitMessage

git push origin main