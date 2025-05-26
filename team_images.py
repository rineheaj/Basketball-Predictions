from PIL import Image
import streamlit as st


def show_team_bg(team1: str, team2: str):
    col1, col2 = st.columns(2)

    try:
        img1 = Image.open(
            f"images\{team1.lower()}.jpg"
        )

        img2 = Image.open(
            f"images\{team2.lower()}"
        )
    except (FileNotFoundError, Exception) as e:
        st.warning("Background image not found for one or both teams.")
        return
    
    with col1:
        st.image(img1, use_container_width=True, caption=team1)

    
    with col2:
        st.image(img2, use_container_width=True, caption=team2)

    