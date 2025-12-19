# spotify-features-patterns
Encoding Music Project
# Audio Features, Genres, and Popularity on Spotify (2000–2019)

This project explores how popular music appears when sound is encoded through Spotify’s audio features and organized by genre and artist. Using a dataset of platform-visible songs from 2000 to 2019, the project examines patterns of similarity, consistency, convergence, and reward across genres and artists.

Rather than evaluating musical quality or listener preference, the analysis focuses on how **platform-defined audio features** structure what becomes legible, comparable, and visible at scale.

## Conceptual Framework

This project is informed by:

- **Nick Seaver (2022)**, who argues that systems used to measure and organize taste do not merely reflect preferences, but actively shape which patterns become visible and meaningful.
- **Amanda Petrusich (2021)**, who shows that genre labels continue to matter culturally even as they become weaker predictors of how music actually sounds.

Taken together, the project asks:

When music is encoded through platform-defined audio features, what patterns of similarity, consistency, and reward emerge across artists and genres?

## Research Questions

- What audio features characterize artists and genres between 2000 and 2019?
- How do genres differ or overlap sonically when measured through Spotify’s features?
- How consistent are artists’ sound signatures within this dataset?
- How do platform-legible features align with visibility and popularity

## Dataset

- **Source:** Kaggle — *Top Hits Spotify from 2000 to 2019*
- **Files used:**
  - `songs_normalize.csv`
  - `songs_expanded_genres.csv` (after genre expansion and cleaning)

This dataset should be understood as a proxy for **platform-visible music**, not a comprehensive record of musical popularity or cultural value.

## Project Structure
-  main.py                     # Streamlit app entry point
- expand_genres.py             # Genre expansion / preprocessing
-  tab2_genre.py                # Genre Taste Worlds
-  tab3_artists.py              # Artist Sound Signatures
- tab4_genre_patterns.py       # Within-genre variation over time
- tab5_popularity.py           # Feature–popularity response curves
- tab6_bubble_chart.py         # Animated genre evolution
- songs_expanded_genres.csv
- songs_normalize.csv
- README.md
