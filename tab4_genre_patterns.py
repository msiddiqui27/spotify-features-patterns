import streamlit as st
import pandas as pd
import plotly.express as px
from tab6_bubble_chart import show_animated_bubble_chart


def calculate_genre_convergence(df, min_songs_per_genre_year=10):
    #measure within-genre variation by year using feature standard deviation
    features = ["energy", "danceability", "valence", "acousticness"]
    grouped = df.groupby(["genre", "year"])

    rows = []

    for (genre, year), group in grouped:
        #skip sparse genre-year groups so the variation estimate is not noisy
        if len(group) < min_songs_per_genre_year:
            continue

        row = {"genre": genre, "year": year, "sample_size": len(group)}

        for feature in features:
            row[f"{feature}_std"] = group[feature].std()

        rows.append(row)

    return pd.DataFrame(rows)


def show_genre_patterns(df):
    """Tab 4: Genre Patterns. Within-Genre Sonic Variation Over Time."""

    st.header("Genre Patterns: Sonic Variation Over Time")

    st.markdown(
        """
        This section examines how **within-genre sonic variation** changes between 2000 and 2019
        using Spotify’s encoded audio features.

        Rather than comparing genres to one another, the focus is on **internal structure**,
        meaning how tightly clustered or diverse songs within the same genre are along
        particular sonic dimensions.
        """
    )
    st.markdown(
        """
        **Operational definition:**  
        Here, convergence refers to decreasing within-genre variation over time,
        measured as a lower within-genre standard deviation for a given feature.
        """
    )

    st.markdown(
        """
        **Method Overview**
        - For each genre and year, the standard deviation of selected audio features is calculated  
          (energy, danceability, valence, acousticness)
        - Lower standard deviation indicates greater similarity among songs within a genre  
        - Higher standard deviation indicates greater internal diversity
        - Genre-year combinations with fewer than 10 songs are excluded to avoid unstable estimates
        """
    )

    st.markdown("---")

    #compute within-genre variation across time
    convergence_df = calculate_genre_convergence(df, min_songs_per_genre_year=10)

    if convergence_df.empty:
        st.error("No genre-year combinations meet the minimum data threshold.")
        return

    valid_genres = sorted(convergence_df["genre"].unique())

    #controls for selecting genres and features
    col1, col2 = st.columns(2)

    with col1:
        selected_genres = st.multiselect(
            "Select genres to display:",
            options=valid_genres,
            default=valid_genres[:2],
            key="genre_patterns_genres",
        )

    with col2:
        selected_feature = st.selectbox(
            "Select feature to analyze:",
            ["energy", "danceability", "valence", "acousticness"],
            key="genre_patterns_feature",
        )

    st.info(
        f"Available genres: {', '.join(valid_genres)}\n\n"
        "Genres not listed here lack sufficient data across years "
        "(minimum 10 songs per genre-year required)."
    )

    filtered_df = convergence_df[convergence_df["genre"].isin(selected_genres)]
    feature_col = f"{selected_feature}_std"

    #plot within-genre variation over time for the selected feature
    fig = px.line(
        filtered_df,
        x="year",
        y=feature_col,
        color="genre",
        markers=True,
        title=f"Standard Deviation of {selected_feature.capitalize()} by Genre",
        labels={"year": "Year", feature_col: "Standard Deviation (Lower Means More Similar)"},
        height=450,
        template="plotly_dark",
    )

    fig.update_traces(line=dict(width=2.5), marker=dict(size=6))
    fig.update_layout(hovermode="x unified")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("How to Read This Chart")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            **Downward trend**
            - Songs within the genre become more similar
            - The acceptable sonic range narrows along this feature
            """
        )

    with col2:
        st.markdown(
            """
            **Flat or upward trend**
            - The genre maintains or expands internal diversity
            - Multiple sonic strategies remain viable
            """
        )

    st.markdown("---")

    st.subheader("Feature Change Summary")

    summary_rows = []

    for genre in filtered_df["genre"].unique():
        g = filtered_df[filtered_df["genre"] == genre].sort_values("year")

        if len(g) > 1:
            start = g[feature_col].iloc[0]
            end = g[feature_col].iloc[-1]
            change = end - start
            pct = (change / start) * 100 if start != 0 else 0

            summary_rows.append(
                {
                    "Genre": genre,
                    f"{selected_feature.capitalize()} Std (Start)": f"{start:.3f}",
                    f"{selected_feature.capitalize()} Std (End)": f"{end:.3f}",
                    "Change": f"{change:.3f}",
                    "% Change": f"{pct:.1f}%",
                }
            )
        else:
            summary_rows.append(
                {
                    "Genre": genre,
                    f"{selected_feature.capitalize()} Std (Start)": f"{g[feature_col].iloc[0]:.3f}",
                    f"{selected_feature.capitalize()} Std (End)": f"{g[feature_col].iloc[0]:.3f}",
                    "Change": "N/A",
                    "% Change": "N/A",
                }
            )

    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

    st.markdown(
        """
        **Interpretation Notes**
        - Negative change indicates convergence along this feature
        - Positive change indicates increasing internal variation
        - N/A indicates insufficient temporal coverage
        """
    )

    st.markdown("---")

    st.subheader("Interpreting the Results")

    st.markdown(
        """
        These results do not show a single, uniform process of genre homogenization.

        Instead, changes in internal variation differ by both genre and feature. For example, Dance/Electronic shows a small increase in within-genre variation in energy between the start and end of the period (from 0.128 to 0.137, a 6.9% increase), suggesting a slight broadening of acceptable energy levels. In contrast, R&B shows a modest decrease in energy variation over time (from 0.138 to 0.134, a 3.0% decrease), indicating increased internal consistency along that feature.

        This pattern demonstrates that convergence is not universal. Genres persist as categories, but the degree to which they stabilize or diversify depends on the specific sonic dimension being measured.
        """)

    st.markdown("---")

    #animated view provides cross-genre context for the broader drift pattern
    show_animated_bubble_chart(df)
