import streamlit as st
from info import show_system_info_modal
from sim_core import highlight_winners
import pandas as pd




def render_system_info_button():
    if st.button("Show System Info"):
        show_system_info_modal()


def inject_custom_styles():
    st.markdown(
        """
        <style>
        @keyframes glow {
            0% { box-shadow: 0 0 15px rgba(255, 0, 0, 0.8), 0 0 30px rgba(255, 0, 0, 0.6), 0 0 45px rgba(255, 0, 0, 0.4); }
            25% { box-shadow: 0 0 15px rgba(0, 255, 0, 0.8), 0 0 30px rgba(0, 255, 0, 0.6), 0 0 45px rgba(0, 255, 0, 0.4); }
            50% { box-shadow: 0 0 15px rgba(0, 0, 255, 0.8), 0 0 30px rgba(0, 0, 255, 0.6), 0 0 45px rgba(0, 0, 255, 0.4); }
            75% { box-shadow: 0 0 15px rgba(255, 165, 0, 0.8), 0 0 30px rgba(255, 165, 0, 0.6), 0 0 45px rgba(255, 165, 0, 0.4); }
            100% { box-shadow: 0 0 15px rgba(128, 0, 128, 0.8), 0 0 30px rgba(128, 0, 128, 0.6), 0 0 45px rgba(128, 0, 128, 0.4); }
        }
    
        .team-img-container {
            border-radius: 15px;
            overflow: hidden;
            padding: 5px;
            margin-bottom: 20px;
            background-color: rgba(255,255,255,0.8);
            animation: glow 6s infinite;
        }
    
        .header {
            color: white;
            background: linear-gradient(to right, #1E90FF, #FFD700);
            text-align: center;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.2);
            font-family: 'Arial', sans-serif;
        }
    
        .stApp {
            background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8));
            background-size: cover;
            background-attachment: fixed;
        }
    
        @keyframes glow-line {
            0% { box-shadow: 0 0 15px rgba(255, 0, 0, 0.9); }
            25% { box-shadow: 0 0 15px rgba(0, 255, 0, 0.9); }
            50% { box-shadow: 0 0 15px rgba(0, 0, 255, 0.9); }
            75% { box-shadow: 0 0 15px rgba(255, 165, 0, 0.9); }
            100% { box-shadow: 0 0 15px rgba(128, 0, 128, 0.9); }
        }
    
        .glow-divider {
            width: 100%;
            height: 6px;
            margin: 20px 0;
            background-color: white;
            border-radius: 5px;
            animation: glow-line 2.5s infinite alternate;
        }
        </style>
    
        <div class="glow-divider"></div>
        """,
        unsafe_allow_html=True
    )


def render_main_header():
    st.markdown(
        '<h1 class="header">🏀 NBA Game Winner Predictions</h1>',
        unsafe_allow_html=True
    )

def render_simulation_results(team1, team2, num_sims, results, game_log, analysis):
    df_results = pd.DataFrame(data=game_log, columns=[team1, team2, "Winner"])
    styled_df = (
        df_results.style
        .apply(highlight_winners, axis=1, args=(team1, team2))
        .background_gradient(subset=[team1, team2], cmap="coolwarm")
        .set_properties(**{"text-align": "center", "font-size": "14px"})
        .set_table_styles([{
            "selector": "th",
            "props": [
                ("background-color", "#f7f7f9"),
                ("color", "#333"),
                ("font-size", "16px"),
                ("border", "1px solid #ccc"),
                ("text-align", "center"),
                ("padding", "8px")
            ]
        }])
    )
    st.dataframe(styled_df)
    st.session_state["results"] = results
    st.session_state["game_log"] = game_log
    st.session_state["analysis"] = analysis
    st.session_state["sim_run"] = True