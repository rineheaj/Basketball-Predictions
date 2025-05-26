from PIL import Image
import streamlit as st
from pathlib import Path

def show_team_bg(team1: str, team2: str):
    col1, col2 = st.columns(2)

    try:
        img1 = Image.open(f"images/{team1.lower()}.jpg")
        img2 = Image.open(f"images/{team2.lower()}.jpg")
    except (FileNotFoundError, Exception) as e:
        st.warning("Background image not found for one or both teams.")
        return
    
    with col1:
        st.image(img1, use_container_width=True, caption=team1)

    
    with col2:
        st.image(img2, use_container_width=True, caption=team2)

def validate_paths(team1, team2):
    team_one_path = Path("images")  / (team1.lower() + ".jpg")
    if team_one_path.exists():
        print(f"Path found: {team_one_path}")

    team_two_path = Path("images") / (team2.lower() + ".jpg")
    if team_two_path.exists():
        print(f"Path found: {team_two_path}")

if __name__ == "__main__":
    team1 = "Thunder"
    team2 = "Timberwolves"

    validate_paths(team1, team2)

