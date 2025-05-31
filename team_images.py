from PIL import Image
import streamlit as st
from pathlib import Path
from typing import List


def apply_opacity(image, opacity=0.9):
    """
    Converts the image to RGBA mode and applies the specified opacity.
    An opacity of 0 means fully transparent, while 1 is fully opaque.
    """
    img = image.convert("RGBA")
    
    alpha_value = int(255 * opacity)
    img.putalpha(alpha_value)
    return img


def show_team_bg(team1: str, team2: str, team3: str, team4: str, opacity=0.9):
    col1, col2 = st.columns(2)

    try:
        img1 = Image.open(f"images/{team1.lower()}.jpg")
        img2 = Image.open(f"images/{team2.lower()}.jpg")
        img3 = Image.open(f"images/{team3.lower()}.jpg")
        img4 = Image.open(f"images/{team4.lower()}.jpg")
    except (FileNotFoundError, Exception) as e:
        st.warning("Background image not found for one or more teams.")
        return

    img1 = apply_opacity(img1, opacity)
    img2 = apply_opacity(img2, opacity)
    img3 = apply_opacity(img3, opacity)
    img4 = apply_opacity(img4, opacity)


    with col1:
        st.image(img1, use_container_width=True, caption=team1)

    with col2:
        st.image(img2, use_container_width=True, caption=team2)


def show_team_bg_improved(teams: List[str], start_index=0, opacity=0.9):
    all_images = []

    for team in teams:
        try:
            img = Image.open(f"images/{team.lower()}.jpg")
            img = apply_opacity(img, opacity)
            all_images.append((team, img))
        except Exception as e:
            st.warning(f"Image for {team} not found or failed to load.")
    
    images_to_display = all_images[start_index:start_index + 2]

    cols = st.columns(2)
    for idx, (team, img) in enumerate(images_to_display):
        with cols[idx]:
            st.markdown("<div class='team-img-container'>", unsafe_allow_html=True)
            st.image(img, use_container_width=True, caption=team)
            st.markdown("</div>", unsafe_allow_html=True)
















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

