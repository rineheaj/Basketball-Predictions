import streamlit as st
import pandas as pd
from sim_core import (
    load_team_stats_improved,
    run_sim,
    quick_analysis,
    highlight_winners
)
from team_images import show_team_bg_improved
from info import show_system_info_modal



if st.button("Show System Info"):
    show_system_info_modal()


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
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <h1 style="
        color: white;
        background: linear-gradient(to right, #1E90FF, #FFD700);
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.2);
        font-family: 'Arial', sans-serif;
    ">
        🏀 NBA Game Winner Predictions
    </h1>
    """,
    unsafe_allow_html=True
)


st.markdown(
        """
        <style>
        .stApp {{
            background: 
                linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8));
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
)


st.markdown(
    """
    <style>
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



def main():
    
    st.sidebar.header("Sim Settings")

    num_sims = st.sidebar.slider(
        "Number of Simulations",
        min_value=100,
        max_value=50_000,
        step=1000,
        value=500
    )


    try:
        stats = load_team_stats_improved("nba_teams_2024.csv")
    except Exception as e:
        st.error(f"Error loading team stats: {e}")
        return

    team_names = list(stats.keys())
    team1 = st.sidebar.selectbox(
        "Select Team 1",
        team_names,
        index=0,
        key="team1"
    )



    team2 = st.sidebar.selectbox(
        "Select Team 2",
        team_names,
        index=1 if team_names[0] == team1 else 0,
        key="team2"
    )

    show_team_bg_improved(teams=[team1, team2])

    if st.sidebar.button("Run Simulation"):
        with st.spinner("Running sims..."):
            results, game_log = run_sim(
                team1, team2, stats, num_sims
            )
            analysis = quick_analysis(
                game_log=game_log,
                team1=team1,
                team2=team2
            )

            df_2 = pd.DataFrame(
                data=game_log,
                columns=[team1, team2, "Winner"]
            )
            styled_df_2 = (
                df_2.style
                    .apply(highlight_winners, axis=1, args=(team1, team2))
                    .background_gradient(subset=[team1, team2], cmap="coolwarm")
                    .set_properties(**{"text-align": "center", "font-size": "14px"})
                    .set_table_styles(
                        [{
                            "selector": "th",
                            "props": [
                                ("background-color", "#f7f7f9"),
                                ("color", "#333"),
                                ("font-size", "16px"),
                                ("border", "1px solid #ccc"),
                                ("text-align", "center"),
                                ("padding", "8px")
                            ]
                        }]
                    )
            )

            st.dataframe(styled_df_2)


            st.session_state["results"] = results
            st.session_state["game_log"] = game_log
            st.session_state["analysis"] = analysis
            st.session_state["sim_run"] = True

    if st.session_state.get("sim_run", False):
        team1 = st.session_state["team1"]
        team2 = st.session_state["team2"]
        results = st.session_state["results"]
        game_log = st.session_state["game_log"]
        analysis = st.session_state["analysis"]

        
        if team1 in results and team2 in results:
            st.markdown("<h3 style='text-align: center;'/style>🏆 Win Chance", unsafe_allow_html=True)
            st.markdown("<div class='glow-divider'></div>", unsafe_allow_html=True)
            
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label=f"{team1} Win Chance", value=f"{results.get(team1, 0) / num_sims * 100:.1f}%", border=True)
            with col2:
                st.metric(label=f"{team2} Win Chance", value=f"{results.get(team2, 0) / num_sims * 100:.1f}%", border=True)

            
            st.markdown("<div class='glow-divider'></div>", unsafe_allow_html=True)
            st.subheader("📊 Average Scores & Insights")
            st.markdown("<div class='glow-divider'></div>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label=f"Avg {team1} Score", value=f"{analysis['avg_scores'].get(team1, 0):.1f}", border=True)
            with col2:
                st.metric(label=f"Avg {team2} Score", value=f"{analysis['avg_scores'].get(team2, 0):.1f}", border=True)
            with col3:
                st.metric(label="Avg Point Differential", value=f"{analysis.get('point_diff', 0):.1f}", border=True)

            
            st.metric(label="Close Games (≤5 points)", value=analysis.get("close_games", 0), border=True)

            st.markdown("<div class='glow-divider'></div>", unsafe_allow_html=True)


            df = pd.DataFrame({
                f"{team1} Score": [log[0] for log in game_log],
                f"{team2} Score": [log[1] for log in game_log]
            })
            st.bar_chart(df, x_label="Number of Sims", y_label="Total Points Scored", use_container_width=True)
        else:
            st.warning("Please re-run the simulation after changing teams.")

if __name__ == "__main__":
    main()
