import streamlit as st
import pandas as pd
import plotly.express as px

def standardize_genre_name(genre):
    #map raw genre labels to display-friendly names
    name_map = {
        'hip hop': 'Hip Hop',
        'pop': 'Pop',
        'rock': 'Rock',
        'dance/electronic': 'Dance/Electronic',
        'r&b': 'R&B',
        'latin': 'Latin',
        'country': 'Country',
        'metal': 'Metal',
        'indie': 'Indie',
        'folk': 'Folk',
        'jazz': 'Jazz',
        'classical': 'Classical',
        'folk/acoustic': 'Folk/Acoustic',
        'world/traditional': 'World/Traditional',
        'easy listening': 'Easy Listening',
        'blues': 'Blues'
    }
    return name_map.get(str(genre).lower(), str(genre).capitalize())


def show_genre_worlds(df):
    """Tab 2: Genre Taste Worlds"""

    #initialize session state so navigation is predictable
    if 'selected_genre' not in st.session_state:
        st.session_state['selected_genre'] = None

    #slightly reduce default streamlit padding for denser layout
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.header("Genre Taste Worlds")

    st.markdown(
        "**Genres group songs into recognizable sonic profiles.** "
        "Selecting a genre highlights how its average audio features compare to the broader Spotify catalog."
    )

    st.caption(
        "This establishes a baseline for later tabs that track within-genre change over time and compare "
        "feature patterns to platform visibility."
    )

    st.markdown("---")

    #identify most represented genres to avoid visual clutter
    top_genres = df['genre'].value_counts().head(12)

    #colors are fixed for readability across tabs
    genre_colors = {
        'Hip Hop': '#00E676',
        'Pop': '#FF1744',
        'Rock': '#AA00FF',
        'Dance/Electronic': '#00B0FF',
        'R&B': '#FFAB00',
        'Latin': '#FF6E40',
        'Country': '#FFD600',
        'Metal': '#424242',
        'Indie': '#F50057',
        'Folk': '#8D6E63',
        'Jazz': '#5C6BC0',
        'Classical': '#7E57C2',
        'Folk/Acoustic': '#A0826D',
        'World/Traditional': '#CD853F',
        'Easy Listening': '#B19CD9',
        'Blues': '#4169E1'
    }

    st.subheader("Top Genres")

    cols = st.columns(3)

    for idx, (genre, count) in enumerate(top_genres.items()):
        display_name = standardize_genre_name(genre)
        bg_color = genre_colors.get(display_name, '#616161')
        genre_data = df[df['genre'] == genre]

        with cols[idx % 3]:
            card_html = f"""
            <div style="
                background: linear-gradient(135deg, {bg_color}22 0%, {bg_color}44 100%);
                border: 1px solid {bg_color}66;
                padding: 16px;
                border-radius: 12px;
                margin: 8px 0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.25);
                min-height: 95px;
            ">
                <h4 style="
                    color: {bg_color};
                    margin: 0 0 6px 0;
                    font-size: 18px;
                    font-weight: 600;
                ">{display_name}</h4>
                <p style="
                    color: rgba(255,255,255,0.8);
                    margin: 0;
                    font-size: 12px;
                ">
                    {count} songs<br>
                    {genre_data['artist'].nunique()} artists
                </p>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

            if st.button(
                f"Explore {display_name}",
                key=f"genre_btn_{idx}",
                use_container_width=True
            ):
                st.session_state['selected_genre'] = genre
                st.rerun()

    st.markdown("---")

    #selected genre view

    if st.session_state['selected_genre']:
        selected = st.session_state['selected_genre']
        genre_data = df[df['genre'] == selected]
        display_name = standardize_genre_name(selected)

        left, right = st.columns([1, 3])

        # left column shows summary metrics
        with left:
            st.subheader(display_name)

            st.metric("Songs", len(genre_data))
            st.metric("Artists", genre_data['artist'].nunique())
            st.metric("Avg Energy", f"{genre_data['energy'].mean():.2f}")
            st.metric("Avg Tempo", f"{genre_data['tempo'].mean():.0f} BPM")

            #use the return value so the button click is handled correctly
            back_clicked = st.button("Back", use_container_width=True)

        #right column shows feature comparison
        with right:
            st.subheader("Sonic Profile vs Overall")

            features = ['danceability', 'energy', 'valence', 'acousticness']

            comparison_df = pd.DataFrame({
                'Feature': features,
                display_name: genre_data[features].mean().values,
                'Overall Average': df[features].mean().values
            })

            fig = px.bar(
                comparison_df,
                x='Feature',
                y=[display_name, 'Overall Average'],
                barmode='group',
                color_discrete_map={
                    display_name: genre_colors.get(display_name, '#1DB954'),
                    'Overall Average': '#888888'
                }
            )

            fig.update_layout(
                height=300,
                hovermode='x unified',
                margin=dict(l=10, r=10, t=30, b=20),
                legend_title_text=""
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

            st.caption("Colored bar shows the genre average. Gray bar shows the overall catalog average.")

        #reset view when navigating back
        if back_clicked:
            st.session_state['selected_genre'] = None
            st.rerun()

        st.markdown(
            "This comparison establishes baseline sonic differences across genres before moving to artist-level patterns, "
            "within-genre change over time, and feature patterns tied to platform visibility."
        )

        st.markdown("---")
