import streamlit as st
import pandas as pd
import plotly.express as px

import tab2_genre
import tab3_artists
from tab4_genre_patterns import show_genre_patterns
from tab5_popularity import show_popularity_mechanisms


st.set_page_config(
    page_title="Audio Features, Genres, and Popularity on Spotify",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data
def load_data():
    df = pd.read_csv("songs_expanded_genres.csv")

    #keep only rows with a clean year, then restrict to the project window
    df = df[df["year"].astype(str).str.isdigit()]
    df["year"] = df["year"].astype(int)
    df = df[(df["year"] >= 2000) & (df["year"] <= 2019)]

    return df


df = load_data()


#sidebar: audio feature reference for reader in case they need to refer back to understand the audio features
with st.sidebar:
    st.title("Spotify Audio Feature Reference")

    with st.expander("Audio Feature Definitions", expanded=False):
        st.markdown("""
        **Danceability (0 to 1):** Suitability for dancing based on rhythm and beat stability  
        **Energy (0 to 1):** Perceived intensity and activity  
        **Valence (0 to 1):** Musical positiveness (happy versus sad)  
        **Acousticness (0 to 1):** Likelihood that the track is acoustic  
        **Tempo (BPM):** Speed of the track  
        **Speechiness (0 to 1):** Presence of spoken words  
        **Loudness (dB):** Overall amplitude  
        **Instrumentalness (0 to 1):** Likelihood of no vocals  
        **Liveness (0 to 1):** Presence of a live audience  
        """)

    st.markdown("---")
    st.caption(
        "These features are computational descriptors of sound. "
        "They do not capture meaning, intent, cultural context, or musical quality."
    )

st.markdown("---")
#title and intro
st.title("Audio Features, Genres, and Popularity on Spotify (2000 to 2019)")
st.markdown("---")

st.markdown("""
### Project Overview

This project examines **audio feature patterns** among popular artists and genres on Spotify
between 2000 and 2019.

Rather than evaluating musical quality or individual listener preferences, the analysis focuses on
how popular music appears when sound is encoded through Spotify’s audio features and organized by
genre and artist.

The project is based on the work of Seaver (2019), who argues that systems used to measure and organize taste
do more than reflect listener preferences, they shape what kinds of patterns become visible and
meaningful in the first place. Additionally, this project draws on Petrusich (2021), who shows that while genre labels
continue to matter culturally, they have become less reliable indicators of how music actually sounds.

Together, these ideas motivate an empirical question: when music is encoded through platform-defined audio features, what patterns of similarity, consistency, and reward emerge across artists and genres?
""")

st.markdown("""
### Research Questions

- What audio features characterize given artists and genres from 2000 to 2019?
- How are genres associated with distinct or overlapping sonic feature profiles?
- How consistent are artists’ sound signatures within the dataset?
- What do similarities and differences across artists and genres suggest about platform-mediated taste formation?
""")

st.info("""
How to navigate this project
1. Begin with Data and Encoding to understand what the dataset contains and what the measures mean  
2. Explore Genre Taste Worlds to see how genres differ sonically  
3. Examine Artist Sound Signatures for consistencies and variations within their genres.
4. Review Genre Patterns to track within-genre variation over time  
5. Use Popularity Mechanisms to test whether the same features also align with visibility  
6. End with Scope and Conclusions for limitations and takeaways  
""")

st.markdown("---")


#tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "1. Data and Encoding",
    "2. Genre Taste Worlds",
    "3. Artist Sound Signatures",
    "4. Genre Patterns",
    "5. Popularity Mechanisms",
    "6. Scope and Conclusions"
])


#tab 1: data
with tab1:
    st.header("Introducing the Dataset and Audio Features")

    st.markdown("""
    This dataset includes songs that achieved **platform visibility** on Spotify between 2000 and 2019.

    In this project, "popularity" is treated as a visibility outcome inside platform systems, not a measure of artistic quality or cultural value. Where the dataset includes Spotify’s popularity score, it is used as a platform-facing indicator. In the popularity tab, I also use a simple within-dataset proxy (how often a song appears after genre expansion) to illustrate how visibility can be operationalized when data is incomplete.
    """)

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Unique Songs", df[["artist", "song"]].drop_duplicates().shape[0])
    with col2:
        st.metric("Years Covered", f"{df['year'].min()} to {df['year'].max()}")
    with col3:
        st.metric("Genres", df["genre"].nunique())
    with col4:
        st.metric("Artists", df["artist"].nunique())

    st.markdown("---")

    st.subheader("Data Notes, Cleaning, and Encoding Choices")

    st.markdown("""
    This project relies on secondary data and makes a few explicit encoding choices:

    - **Source:** The dataset is a Kaggle compilation of Spotify "top hits" metadata, which makes it useful for exploratory platform analysis but not fully transparent about inclusion criteria.
    - **Time window:** Rows are filtered to years 2000 through 2019 using the `year` column.
    - **Genre expansion:** The file used here is `songs_expanded_genres.csv`, which represents songs after genre labels were expanded into cleaner categories. This supports comparison across a small number of consistent genres instead of many sparse tags.
    - **Avoiding duplication:** When the same song appears multiple times due to genre expansion, unique artist strings were considered to avoid redundancies and incorrect information.
    - **What the features mean:** Audio features are treated as platform-legible measurements, not full descriptions of musical experience.
    """)

    st.markdown("---")

    st.subheader("What Can and Cannot Be Claimed")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **This analysis can examine:**
        - Audio feature patterns in platform-visible music  
        - Differences and overlaps across genres  
        - Consistency within artists’ sound profiles  
        - Associations between encoded features and visibility measures  
        """)
    with col2:
        st.markdown("""
        **This analysis does not claim:**
        - Musical quality or aesthetic value  
        - Listener intent or motivation  
        - Direct causal relationships  
        - Complete representation of all musical production  
        """)

    st.markdown("---")

    st.subheader("Listener's Intuition")

    st.markdown("""
    A practical goal of encoding music is to compare quantitative patterns to common listening intuitions. For example, a listener might expect rock to be less danceable than pop, or dance and electronic genres to cluster at higher energy levels. The genre and artist tabs make these expectations explicit and show where encoded features align with them and where they break down.    """)

    st.markdown("---")

    st.subheader("Feature Distributions")

    feature = st.selectbox(
        "Select a feature",
        ["danceability", "energy", "valence", "acousticness", "tempo", "speechiness", "loudness"]
    )

    fig = px.histogram(
        df,
        x=feature,
        nbins=40,
        title=f"Distribution of {feature.capitalize()} Across Platform-Visible Songs"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "These distributions provide context for the range of audio feature values present in the dataset and help ground later comparisons between genres, artists, and popularity patterns."
    )


#tab 2: genres
with tab2:
    tab2_genre.show_genre_worlds(df)


#tab 3: artists
with tab3:
    tab3_artists.show_artist_signatures(df)


#tab 4: genre patterns
with tab4:
    show_genre_patterns(df)


#tab 5: popularity mechanisms
with tab5:
    show_popularity_mechanisms(df)


#tab 6: conclusion
with tab6:
    st.header("Scope, Limitations, and Conclusions")

    st.subheader("Scope and Limitations")
    st.markdown("""
    This project analyzes Spotify audio features as computational representations of sound, not exhaustive descriptions of musical experience. These features capture aspects of timbre, rhythm, and intensity that are legible to platforms, but they do not account for lyrics, cultural context, listener interpretation, or embodied experience.

    The dataset used in this analysis was sourced from a publicly available Kaggle dataset,
    [Top Hits Spotify from 2000 to 2019](https://www.kaggle.com/datasets/paradisejoy/top-hits-spotify-from-20002019).
    While useful for exploratory analysis, the dataset reflects limitations of secondary data: the criteria for inclusion, the definition of "top hits," and the construction of popularity measures are not fully transparent. As a result, this dataset should be understood as a proxy for platform-visible music rather than a comprehensive record of musical popularity.

    Measures of popularity in this project reflect platform visibility and circulation, not artistic quality, listener preference, or cultural value. Popularity here is best understood as an outcome shaped by recommendation, playlisting, and exposure, rather than a proxy for merit.

    A further limitation is that the dataset records the year a song was released, not the year it became popular. Songs that gain traction well after release are therefore anchored to their release date, which can blur the timing of observed trends. Future work could address this by incorporating time-series streaming data, chart trajectories, or playlist histories to separate release from circulation and visibility.

    Genre labels are treated as platform-assigned categories that organize music for discovery and analysis. These labels may shift over time, overlap in practice, or fail to capture how artists and listeners understand genre boundaries.

    Observed relationships between audio features, genre patterns, and popularity are descriptive, not causal. This analysis does not claim that specific features cause success, nor that algorithms directly dictate artistic choices.

    Finally, this project focuses on music that appears on a major streaming platform. Music circulated outside dominant platforms, informal scenes, or non-digitized contexts is necessarily underrepresented.
    """)

    st.markdown("---")

    st.subheader("Conclusion")
    st.markdown("""
    This project documents patterned regularities in the audio features of platform-visible music on Spotify between 2000 and 2019.

    Across genres and artists, the analysis shows recognizable sonic profiles, varying degrees of internal consistency, and selective convergence along platform-legible dimensions of sound. Rather than collapsing genres into a single form, the results suggest that genres persist while becoming less predictive of variation along the features that most directly structure visibility in this dataset.

    Read alongside Seaver and Petrusich, the project treats encoded features and labels as cultural infrastructure, meaning they help organize what becomes legible, comparable, and surfaced at scale. The findings support a cautious interpretation: platform logics may not determine what artists make, but they can shape what kinds of sound become easier to circulate, repeat, and recognize within platform-defined categories.
    """)
    st.markdown("---")
