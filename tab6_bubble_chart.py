import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def prepare_bubble_data(df):
    """
    prepare genre-year data for bubble chart
    """

    #aggregate by genre and year using mean feature values
    bubble_data = df.groupby(['genre', 'year']).agg({
        'danceability': 'mean',
        'energy': 'mean',
        'song': 'count'  #number of songs per genre-year
    }).reset_index()

    bubble_data = bubble_data.rename(columns={'song': 'song_count'})

    return bubble_data


def show_animated_bubble_chart(df):
    """
    animated bubble chart showing genre movement through feature space
    """

    st.subheader("Animated Genre Evolution: The 20-Year Drift")

    st.markdown("""
    Watch how genres move through feature space between 2000 and 2019.

    Each point represents a genre’s **average position** in danceability–energy
    space for a given year. The animation demonstrates whether genres remain
    separated or move toward similar sonic regions over time.
    """)

    #prepare aggregated genre-year data
    bubble_df = prepare_bubble_data(df)

    #fixed color mapping to keep genre identity stable across frames
    genre_colors = {
        'Dance/Electronic': '#1DB954',
        'Hip Hop': '#FF6B6B',
        'Metal': '#95A5A6',
        'Pop': '#FFD93D',
        'R&B': '#6C5CE7',
        'Rock': '#00B4D8'
    }

    #animated scatter plot
    fig = px.scatter(
        bubble_df,
        x='danceability',
        y='energy',
        animation_frame='year',
        animation_group='genre',
        size='song_count',
        color='genre',
        hover_name='genre',
        hover_data={
            'danceability': ':.3f',
            'energy': ':.3f',
            'song_count': True,
            'year': False,
            'genre': False
        },
        range_x=[0, 1],
        range_y=[0, 1],
        size_max=60,
        color_discrete_map=genre_colors,
        title="Genre Evolution in Feature Space (2000–2019)",
        labels={
            'danceability': 'Danceability',
            'energy': 'Energy',
            'song_count': 'Songs'
        },
        height=600
    )

    #layout tweaks for readability and consistency
    fig.update_layout(
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(200, 200, 200, 0.2)',
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(200, 200, 200, 0.2)',
            zeroline=False
        ),
        hovermode='closest',
        template='plotly_dark',
        font=dict(size=12),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(0,0,0,0.5)",
            bordercolor="white",
            borderwidth=1
        )
    )

    #quadrant annotations for interpretive reference
    fig.add_annotation(
        text="low dance<br>low energy",
        x=0.25, y=0.25,
        showarrow=False,
        font=dict(size=10, color="rgba(255,255,255,0.3)"),
        xref="x domain", yref="y domain"
    )

    fig.add_annotation(
        text="high dance<br>high energy",
        x=0.75, y=0.75,
        showarrow=False,
        font=dict(size=10, color="rgba(255,255,255,0.3)"),
        xref="x domain", yref="y domain"
    )

    st.plotly_chart(fig, use_container_width=True, key="genre_evolution_bubble")

    st.markdown("---")

    #interpretation
    st.subheader("Reading the Animation: What Convergence Looks Like")

    st.markdown("""
    Across the 2000 to 2019 period, genre averages move in similar directions along danceability and energy. Genres that start out more separated gradually shift closer together, especially after the late 2000s. This means that the average sound of different genres becomes more similar over time, even though they do not collapse into a single, uniform sound.

    The visualization shows convergence in average position rather than full homogenization. Genres remain distinguishable, but the distance between them narrows as more songs cluster around higher danceability and moderate to high energy.

    This pattern helps explain how platform-relevant features matter. Danceability and energy are not just descriptive traits. They are also used to organize, recommend, and surface music on Spotify. Over time, these features appear to become reference points for visibility, shaping which sounds are more likely to circulate and reappear on the platform.

    In line with Petrusich’s argument, genres continue to exist as labels, but their ability to signal sound becomes weaker. Genre does not disappear. Instead, it becomes less reliable as a predictor of how music will sound along the specific audio features emphasized by the platform.

    """)

    st.markdown("---")