import streamlit as st
import pandas as pd
import plotly.express as px


#helper functions

def categorize_feature(value, feature_type="normalized"):
    #convert continuous features into coarse categories for interpretability
    #this makes patterns readable without treating small numeric differences as meaningful
    if feature_type == "normalized":
        if value >= 0.66:
            return "High"
        if value >= 0.33:
            return "Medium"
        return "Low"

    if feature_type == "tempo":
        if value >= 130:
            return "High"
        if value >= 90:
            return "Medium"
        return "Low"

    #function always returns something
    return "Medium"


def create_sonic_signature(row):
    #summarize a song using simplified feature labels for quick scanning
    features = ["energy", "danceability", "valence", "acousticness"]
    parts = []
    for f in features:
        level = categorize_feature(row[f], "normalized")
        parts.append(f"{level} {f.capitalize()}")
    return " • ".join(parts)


def show_artist_signatures(df):
    """Tab 3: Artist Sound Signatures"""

    if "selected_artist" not in st.session_state:
        st.session_state["selected_artist"] = None

    selected_artist = st.session_state["selected_artist"]

    #artist selection view
    if not selected_artist:
        st.header("Artist Sound Signatures")

        st.markdown(
            """
            This section examines highly represented artists in the dataset.
            This does not measure an artist’s quality or overall popularity. It reflects what is included in the Kaggle dataset.
            """
        )

        st.markdown("---")

        #rank artists by unique songs to avoid overweighting repeats
        artist_song_counts = (
            df[["artist", "song"]]
            .drop_duplicates()
            .groupby("artist")
            .size()
            .sort_values(ascending=False)
            .head(20)
        )

        st.subheader("Top Artists by Unique Songs")

        cols = st.columns(4)

        for idx, (artist, song_count) in enumerate(artist_song_counts.items()):
            artist_data = df[df["artist"] == artist]

            #deduplicate by song so feature summaries reflect songs, not rows
            deduped = artist_data.drop_duplicates(subset=["song"])
            avg_pop = deduped["popularity"].mean()

            if avg_pop >= 70:
                color = "#1DB954"
            elif avg_pop >= 50:
                color = "#1E88E5"
            else:
                color = "#757575"

            with cols[idx % 4]:
                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(135deg, {color}22, {color}44);
                        border: 1px solid {color}66;
                        padding: 16px;
                        border-radius: 12px;
                        margin-bottom: 8px;
                    ">
                        <strong style="color:{color}">{artist}</strong><br>
                        {song_count} songs<br>
                        Avg popularity: {avg_pop:.0f}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(f"Explore {artist}", key=f"artist_{idx}", use_container_width=True):
                    st.session_state["selected_artist"] = artist
                    st.rerun()

    #artist detail view
    else:
        artist_data = df[df["artist"] == selected_artist]

        #deduplicate songs for feature summaries
        deduped = artist_data.drop_duplicates(subset=["song"]).copy()
        features = ["energy", "danceability", "valence", "acousticness"]

        col1, col2 = st.columns([1, 6])

        with col1:
            #use a stable unique key so streamlit does not generate a duplicate element id
            if st.button("Back", key="artist_back_button", use_container_width=True):
                st.session_state["selected_artist"] = None
                st.rerun()

        with col2:
            st.title(selected_artist)

        st.markdown("---")

        st.subheader("Overview and Sonic Profile")

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            st.metric("Songs", deduped.shape[0])
        with c2:
            st.metric("Genres", artist_data["genre"].nunique())
        with c3:
            st.metric("Avg Popularity", f"{deduped['popularity'].mean():.0f}")
        with c4:
            st.metric("Avg Energy", f"{deduped['energy'].mean():.2f}")
        with c5:
            st.metric("Avg Tempo", f"{deduped['tempo'].mean():.0f} BPM")

        averages = deduped[features].mean()

        #convert averages into a readable sonic profile
        signature = " • ".join(
            f"{categorize_feature(averages[f])} {f.capitalize()}" for f in features
        )

        st.markdown(
            f"""
            <div style="
                background:#1DB95420;
                border-left:4px solid #1DB954;
                padding:12px;
                border-radius:6px;
                margin-top:10px;
            ">
                <strong>Derived Sonic Profile:</strong><br>
                <code>{signature}</code>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("----")

        st.subheader("Sound Consistency (Feature Variation)")

        st.markdown(
        """
            **Sound Consistency (Feature Variation)**

            This chart summarizes how consistent an artist’s sound is across songs for each feature.
            For each feature, consistency is calculated by measuring how much the artist’s songs vary
            and then inverting that value.

            Higher bars indicate that an artist’s songs cluster closely together along that feature,
            while lower bars indicate greater variation across songs.

            In other words, this shows whether an artist tends to reuse a similar sonic profile
            or experiments more widely along a given dimension.
        """)

        #estimate consistency by inverting feature-level standard deviation
        consistency = []
        for f in features:
            std = deduped[f].std()
            consistency.append({"Feature": f.capitalize(), "Consistency": 1 - min(std, 1)})

        consistency_df = pd.DataFrame(consistency)

        fig = px.bar(
            consistency_df,
            x="Feature",
            y="Consistency",
            range_y=[0, 1],
            color="Consistency",
            color_continuous_scale="Greens",
        )
        fig.update_layout(height=320, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        st.subheader("Feature Distribution")

        feature = st.selectbox(
            "Select feature",
            features,
            format_func=lambda x: x.capitalize(),
            key="artist_feature_select",
        )

        fig = px.histogram(
            deduped,
            x=feature,
            nbins=15,
            color_discrete_sequence=["#1DB954"],
        )
        fig.update_layout(height=320, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        st.subheader("Genre Representation")

        #keep genre counts consistent with the deduped definition of songs
        genre_counts = (
        artist_data.groupby("genre")
        .agg(Songs=("song", "nunique"), Avg_Popularity=("popularity", "mean"))
        .reset_index()
        .sort_values("Songs", ascending=False)
    )

        fig = px.bar(
            genre_counts,
            x="genre",
            y="Songs",
            color="Avg_Popularity",
            color_continuous_scale="Viridis",
        )
        fig.update_layout(height=320)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        st.subheader("All Songs")

        table = deduped[
            ["song", "genre", "popularity", "energy", "danceability", "valence", "acousticness"]
        ].copy()

        table["Sonic Profile"] = table.apply(create_sonic_signature, axis=1)

        st.dataframe(
            table.sort_values("popularity", ascending=False),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("---")
